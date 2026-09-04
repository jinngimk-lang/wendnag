from zipfile import ZipFile, ZIP_DEFLATED
from lxml import etree
import re, sys

W='http://schemas.openxmlformats.org/wordprocessingml/2006/main'
V='urn:schemas-microsoft-com:vml'
NS={'w':W,'v':V}

def q(ns,tag): return f'{{{ns}}}{tag}'

def parse_style(s):
    return [part.strip() for part in (s or '').split(';') if part.strip()]

def set_style_prop(el,key,val):
    parts=[]; found=False
    for p in parse_style(el.get('style')):
        if ':' in p and p.split(':',1)[0].strip().lower()==key.lower():
            parts.append(f'{key}:{val}'); found=True
        else:
            parts.append(p)
    if not found:
        parts.append(f'{key}:{val}')
    el.set('style',';'.join(parts))

def set_run_size(shape,pt):
    hp=str(int(round(pt*2)))
    for rpr in shape.xpath('.//w:rPr',namespaces=NS):
        sz=rpr.find(q(W,'sz'))
        if sz is None: sz=etree.SubElement(rpr,q(W,'sz'))
        sz.set(q(W,'val'),hp)
        szc=rpr.find(q(W,'szCs'))
        if szc is None: szc=etree.SubElement(rpr,q(W,'szCs'))
        szc.set(q(W,'val'),hp)

def patch(src,out):
    with ZipFile(src) as zin, ZipFile(out,'w',ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data=zin.read(item.filename)
            if item.filename=='word/document.xml':
                root=etree.fromstring(data)
                for tb in root.xpath('//v:textbox',namespaces=NS):
                    tb.set('inset','0.25pt,0.15pt,0.25pt,0.15pt')
                    set_style_prop(tb,'mso-fit-text-to-shape','t')
                    set_style_prop(tb,'mso-fit-shape-to-text','f')
                    for sp in tb.xpath('.//w:spacing',namespaces=NS):
                        sp.set(q(W,'before'),'0'); sp.set(q(W,'after'),'0')
                        sp.set(q(W,'line'),'180'); sp.set(q(W,'lineRule'),'auto')
                for i in range(5):
                    els=root.xpath(f'//*[@id="f15_name{i}"]')
                    if els:
                        el=els[0]; st=el.get('style','')
                        st=re.sub(r'top:[^;]+','top:1260',st)
                        st=re.sub(r'height:[^;]+','height:340',st)
                        el.set('style',st); set_run_size(el,6.6)
                    els=root.xpath(f'//*[@id="f15_amt{i}"]')
                    if els:
                        el=els[0]; st=el.get('style','')
                        st=re.sub(r'top:[^;]+','top:1640',st)
                        st=re.sub(r'height:[^;]+','height:190',st)
                        el.set('style',st); set_run_size(el,7.2)
                for i in range(3):
                    for j in range(3):
                        els=root.xpath(f'//*[@id="f16_b{i}_{j}"]')
                        if els:
                            el=els[0]; st=el.get('style','')
                            st=re.sub(r'height:[^;]+','height:185',st)
                            el.set('style',st); set_run_size(el,5.5)
                data=etree.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
            zout.writestr(item,data)

if __name__=='__main__':
    patch(sys.argv[1],sys.argv[2])
