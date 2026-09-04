from zipfile import ZipFile, ZIP_DEFLATED
from lxml import etree
from pathlib import Path
import sys

W='http://schemas.openxmlformats.org/wordprocessingml/2006/main'
V='urn:schemas-microsoft-com:vml'
O='urn:schemas-microsoft-com:office:office'
W10='urn:schemas-microsoft-com:office:word'
MC='http://schemas.openxmlformats.org/markup-compatibility/2006'
NS={'w':W,'v':V,'mc':MC}

NAVY='17365D'; BLUE='2F75B5'; PALE='EAF2F8'; BORDER='A9C4DC'; TEXT='263645'; MUTED='68798A'; LIGHT='DCEBF7'; WHITE='FFFFFF'
FONT='Microsoft YaHei'


def q(ns,tag): return f'{{{ns}}}{tag}'


def set_style(e, **kw):
    parts=[]
    for k,v in kw.items():
        parts.append(f"{k.replace('_','-')}:{v}")
    e.set('style',';'.join(parts))


def textbox(parent, text_value, size=10, bold=False, color=TEXT, align='center'):
    tb=etree.SubElement(parent,q(V,'textbox')); tb.set('inset','1pt,1pt,1pt,1pt')
    tx=etree.SubElement(tb,q(W,'txbxContent'))
    p=etree.SubElement(tx,q(W,'p'))
    ppr=etree.SubElement(p,q(W,'pPr'))
    sp=etree.SubElement(ppr,q(W,'spacing')); sp.set(q(W,'before'),'0'); sp.set(q(W,'after'),'0'); sp.set(q(W,'line'),'180'); sp.set(q(W,'lineRule'),'auto')
    jc=etree.SubElement(ppr,q(W,'jc')); jc.set(q(W,'val'),{'left':'left','right':'right'}.get(align,'center'))
    for i,line_value in enumerate(str(text_value).split('\n')):
        r=etree.SubElement(p,q(W,'r')); rpr=etree.SubElement(r,q(W,'rPr'))
        rf=etree.SubElement(rpr,q(W,'rFonts')); rf.set(q(W,'ascii'),'Aptos'); rf.set(q(W,'hAnsi'),'Aptos'); rf.set(q(W,'eastAsia'),FONT)
        if bold: etree.SubElement(rpr,q(W,'b'))
        c=etree.SubElement(rpr,q(W,'color')); c.set(q(W,'val'),color)
        sz=etree.SubElement(rpr,q(W,'sz')); sz.set(q(W,'val'),str(int(round(size*2))))
        szc=etree.SubElement(rpr,q(W,'szCs')); szc.set(q(W,'val'),str(int(round(size*2))))
        t=etree.SubElement(r,q(W,'t')); t.text=line_value
        if i < len(str(text_value).split('\n'))-1: etree.SubElement(r,q(W,'br'))
    return tb


def rect(g,id_value,x,y,w,h,text_value='',fill=WHITE,stroke=BORDER,sw=1,roundrect=True,size=9,bold=False,color=TEXT,align='center'):
    tag='roundrect' if roundrect else 'rect'; e=etree.SubElement(g,q(V,tag)); e.set('id',id_value)
    if roundrect: e.set('arcsize','8%')
    e.set('fillcolor','#'+fill); e.set('strokecolor','#'+stroke); e.set('strokeweight',f'{sw}pt')
    set_style(e,position='absolute',left=str(x),top=str(y),width=str(w),height=str(h),**{'v-text-anchor':'middle'})
    if text_value: textbox(e,text_value,size,bold,color,align)
    return e


def text(g,id_value,x,y,w,h,text_value,size=9,bold=False,color=TEXT,align='center'):
    e=etree.SubElement(g,q(V,'rect')); e.set('id',id_value); e.set('stroked','f'); e.set('filled','f')
    set_style(e,position='absolute',left=str(x),top=str(y),width=str(w),height=str(h),**{'v-text-anchor':'middle'})
    textbox(e,text_value,size,bold,color,align); return e


def line(g,id_value,x1,y1,x2,y2,color=BLUE,sw=1,arrow=False):
    e=etree.SubElement(g,q(V,'line')); e.set('id',id_value); e.set('from',f'{x1},{y1}'); e.set('to',f'{x2},{y2}'); e.set('strokecolor','#'+color); e.set('strokeweight',f'{sw}pt')
    st=etree.SubElement(e,q(V,'stroke')); st.set('color','#'+color); st.set('weight',f'{sw}pt')
    if arrow: st.set('endarrow','block'); st.set('endarrowwidth','narrow'); st.set('endarrowlength','short')
    return e


def oval(g,id_value,x,y,w,h,fill=WHITE,stroke=BLUE,sw=1):
    e=etree.SubElement(g,q(V,'oval')); e.set('id',id_value); e.set('fillcolor','#'+fill); e.set('strokecolor','#'+stroke); e.set('strokeweight',f'{sw}pt')
    set_style(e,position='absolute',left=str(x),top=str(y),width=str(w),height=str(h)); return e


def group(fig,width,height,pt_w,pt_h):
    pict=etree.Element(q(W,'pict'),nsmap={'w':W,'v':V,'o':O,'w10':W10})
    g=etree.SubElement(pict,q(V,'group')); g.set('id',f'fig{fig:02d}_group'); g.set('alt',f'Editable_Figure_{fig}'); g.set('coordorigin','0,0'); g.set('coordsize',f'{width},{height}')
    set_style(g,position='relative',width=f'{pt_w}pt',height=f'{pt_h}pt'); return pict,g


def title(g,fig,w,label):
    text(g,f'f{fig}_title',400,80,w-800,340,label,16,True,NAVY)
    line(g,f'f{fig}_titleline',w//2-260,470,w//2+260,470,BLUE,2)


def fig1():
    Wd,H=5650,3000; pict,g=group(1,Wd,H,406.8,216.0); title(g,1,Wd,'三层产品构成同一套企业智能底座')
    cards=[(220,'组织级','AragonTeam','企业 AI 原生协同工作站'),(2050,'通用级','AegisClaw','线上安全通用智能体'),(3880,'行业级','LegalLens','智能合同审核系统')]
    for i,(x,lv,n,desc) in enumerate(cards):
        rect(g,f'f1_card{i}',x,650,1550,720,'',WHITE,BORDER,1,True)
        text(g,f'f1_lv{i}',x+90,700,1370,110,lv,8.7,True,NAVY); line(g,f'f1_sep{i}',x+130,855,x+1420,855,BORDER,.7)
        text(g,f'f1_name{i}',x+90,900,1370,130,n,10.0,True,NAVY)
        text(g,f'f1_desc{i}',x+90,1160,1370,90,desc,5.8,False,TEXT)
        line(g,f'f1_down{i}',x+775,1370,x+775,1640,BLUE,1.1,True)
    rect(g,'f1_base',220,1680,5210,820,'',PALE,BORDER,1,True)
    text(g,'f1_base_title',500,1730,4650,150,'统一企业智能底座｜四类企业级要件',9.2,True,NAVY)
    for i,h in enumerate(['身份与权限','知识与上下文','流程与状态','审计与留痕']):
        x=390+i*1240; rect(g,f'f1_item{i}',x,2050,1090,260,h,WHITE,BORDER,.8,True,7.2,True,NAVY)
    text(g,'f1_bottom',450,2630,4750,130,'组织级管约束｜通用级管执行｜行业级管领域深度',7.0,True,NAVY)
    return pict,216.0


def fig2():
    Wd,H=5450,3450; pict,g=group(2,Wd,H,392.4,248.4); title(g,2,Wd,'企业级 Agentic AI 市场规模')
    x0,y0=900,2900; top=720; right=4850
    for v in range(0,501,100):
        y=y0-(y0-top)*v/500; line(g,f'f2_grid{v}',x0,int(y),right,int(y),'DCE7F0',.6); text(g,f'f2_y{v}',450,int(y)-70,360,140,str(v),7.5,False,NAVY,'right')
    line(g,'f2_yaxis',x0,top,x0,y0,NAVY,1.0); line(g,'f2_xaxis',x0,y0,right,y0,NAVY,1.0)
    h1=int((y0-top)*67.6/500); h2=int((y0-top)*460.4/500)
    rect(g,'f2_bar1',1400,y0-h1,700,h1,'',PALE,BLUE,1,False); rect(g,'f2_bar2',3600,y0-h2,700,h2,'',LIGHT,BLUE,1,False)
    text(g,'f2_v1',1300,y0-h1-210,900,180,'67.6',12,True,NAVY); text(g,'f2_v2',3500,y0-h2-210,900,180,'460.4',12,True,NAVY)
    text(g,'f2_x1',1250,2950,1000,200,'2025 年',9.5,False,NAVY); text(g,'f2_x2',3380,2950,1150,200,'2030 年（预测）',9.5,False,NAVY)
    rect(g,'f2_cagr',2230,1550,1100,540,'年复合增长率\n47%',WHITE,BLUE,1.2,True,11,True,NAVY); line(g,'f2_arrow',3300,1740,3950,1100,BLUE,1.2,True)
    text(g,'f2_source',1200,3210,3200,160,'数据来源：MarketsandMarkets｜按原 BP 口径',8,False,MUTED)
    return pict,248.4


def fig3():
    Wd,H=5650,2900; pict,g=group(3,Wd,H,406.8,208.8); title(g,3,Wd,'企业 AI 能力四级阶梯')
    steps=[('L1 对话问答','回答问题'),('L2 助手辅助','补全与草拟'),('L3 智能体执行','执行多步任务'),('L4 组织智能','进入权限与流程')]
    xs=[130,1470,2810,4150]; ys=[1510,1330,1150,970]
    for i,((h,a),x,y) in enumerate(zip(steps,xs,ys)):
        rect(g,f'f3_step{i}',x,y,1230,540,'',WHITE,BORDER,1,True)
        text(g,f'f3_h{i}',x+60,y+70,1110,110,h,8.5,True,NAVY); line(g,f'f3_sep{i}',x+100,y+240,x+1130,y+240,BORDER,.7)
        text(g,f'f3_a{i}',x+70,y+330,1090,100,a,6.4,False,TEXT)
        if i<3: line(g,f'f3_arr{i}',x+1230,y+270,xs[i+1],ys[i+1]+270,BLUE,1.0,True)
    text(g,'f3_reqtitle',550,2170,4550,130,'迈向 L4 需要补齐四类企业级要件',8.0,True,NAVY)
    for i,r in enumerate(['身份与权限','知识与上下文','流程与状态','审计与留痕']): rect(g,f'f3_req{i}',430+i*1210,2400,1050,250,r,PALE,BORDER,.8,True,7.3,True,NAVY)
    return pict,208.8


def fig10():
    Wd,H=5650,2450; pict,g=group(10,Wd,H,406.8,176.4); title(g,10,Wd,'公司层面的三种交付形态')
    cards=[('I 私有化服务器部署','企业内网闭环','身份 / 权限 / 审计','总部级客户'),('II 便携式一体机','本地模型 + AI 算力','断网 / 现场部署','项目现场 / 无外网'),('III 私有云服务','私有网络完整能力','集中管理 / 网络边界','公司与团队办公')]
    for i,(h,l1,l2,foot) in enumerate(cards):
        x=190+i*1810; rect(g,f'f10_card{i}',x,700,1590,1050,'',WHITE,BORDER,1,True)
        text(g,f'f10_h{i}',x+70,760,1450,120,h,7.8,True,NAVY); line(g,f'f10_sep{i}',x+110,935,x+1480,935,BORDER,.7)
        text(g,f'f10_l1{i}',x+90,1080,1410,100,l1,6.1,True,TEXT); text(g,f'f10_l2{i}',x+90,1270,1410,100,l2,5.8,False,MUTED)
        rect(g,f'f10_foot{i}',x+170,1480,1250,180,foot,PALE,BORDER,.7,True,5.9,True,NAVY)
    text(g,'f10_bottom',400,1980,4850,130,'AegisClaw 在线上云端提供；行业级合约智审支持公有云与私有化',6.7,True,NAVY)
    return pict,176.4


def fig11():
    Wd,H=5650,3250; pict,g=group(11,Wd,H,406.8,234); title(g,11,Wd,'合约智审系统四层架构')
    layers=[('应用层',['智能审查','上下游一致性','资信审查','文稿智审','合同生成','知识库']),('核心服务层',['文档解析','知识抽取','知识图谱','规则引擎','多智能体协同','垂直大模型']),('技术架构层',['前端框架','后端服务','存储与检索','部署与运维']),('基础层',['算力资源','存储资源'])]
    ys=[720,1260,1800,2340]
    for ri,((lname,items),y) in enumerate(zip(layers,ys)):
        rect(g,f'f11_layerbg{ri}',180,y,5290,430,'',PALE if ri%2==0 else WHITE,BORDER,.8,True); text(g,f'f11_label{ri}',220,y+80,900,270,lname,10,True,NAVY); line(g,f'f11_vsep{ri}',1170,y+65,1170,y+365,BORDER,.7)
        n=len(items); start=1250; avail=4060; gap=50; iw=(avail-gap*(n-1))/n
        for j,it in enumerate(items): rect(g,f'f11_item{ri}_{j}',int(start+j*(iw+gap)),y+105,int(iw),220,it,WHITE,BORDER,.6,True,6.5,ri<2,TEXT)
        if ri<3: line(g,f'f11_down{ri}',2825,y+430,2825,ys[ri+1],BLUE,.9,True)
    text(g,'f11_bottom',500,2940,4650,160,'基础资源 → 技术架构 → 核心服务 → 应用能力，四层职责清晰解耦',8,False,MUTED)
    return pict,234


def fig12():
    Wd,H=5650,2850; pict,g=group(12,Wd,H,406.8,205.2); title(g,12,Wd,'收入结构与客户复制路径')
    text(g,'f12_ltitle',120,650,1450,130,'四条收入线',8.8,True,NAVY); text(g,'f12_rtitle',4080,650,1450,130,'三条复制路径',8.8,True,NAVY)
    left=[('私有化部署软件授权',900),('便携式一体机',1280),('云服务订阅',1660),('行业实施 / 规则库 / 运维',2040)]
    for i,(label,y) in enumerate(left):
        rect(g,f'f12_l{i}',140,y,1500,250,label,WHITE,BORDER,.9,True,6.6,True,TEXT); line(g,f'f12_la{i}',1640,y+125,2150,1510,BLUE,.9,True)
    rect(g,'f12_center',2150,1040,1350,950,'',PALE,BORDER,1,True)
    text(g,'f12_ct',2250,1110,1150,120,'标准化实施方法',8.2,True,NAVY); line(g,'f12_csep',2360,1290,3290,1290,BORDER,.7)
    text(g,'f12_c1',2280,1450,1090,100,'首单共建规则库',5.8,True,TEXT); text(g,'f12_c2',2280,1650,1090,100,'沉淀模板 / 图谱',5.6,False,TEXT); text(g,'f12_c3',2280,1840,1090,100,'形成领域资产',5.6,False,TEXT)
    right=[('战略渠道复制','继承已验证口径',930),('行业样板复制','通信 / 交通量化样板',1500),('政企触点','技术评审 / 试点立项',2070)]
    for i,(h,b,y) in enumerate(right):
        rect(g,f'f12_r{i}',4020,y,1450,360,'',WHITE,BORDER,.9,True); text(g,f'f12_rh{i}',4090,y+65,1310,90,h,6.9,True,NAVY); text(g,f'f12_rb{i}',4090,y+215,1310,80,b,5.5,False,TEXT); line(g,f'f12_ra{i}',3500,1510,4020,y+180,BLUE,.9,True)
    text(g,'f12_bottom',400,2540,4850,130,'同一行业第 N 个客户不必从零起步：复制越多，单位实施投入越低',6.7,True,NAVY)
    return pict,205.2


def fig15():
    Wd,H=5650,2100; pict,g=group(15,Wd,H,406.8,151.2); title(g,15,Wd,'融资资金用途结构（合计 1000 万元）')
    seg=[(.40,'40%','产品研发与\n技术攻关','400 万元'),(.20,'20%','市场与\n渠道建设','200 万元'),(.20,'20%','交付与\n实施团队','200 万元'),(.12,'12%','一体机产品化\n与备货','120 万元'),(.08,'8%','运营储备','80 万元')]
    x=250; total=5150
    for i,(p,pct,name,amt) in enumerate(seg):
        w=round(total*p); rect(g,f'f15_seg{i}',x,800,w,420,pct,LIGHT if i==0 else PALE,BLUE,.8,False,10.5,True,NAVY); x+=w
    legend_x=[300,1320,2340,3360,4380]
    for i,((p,pct,name,amt),lx) in enumerate(zip(seg,legend_x)):
        text(g,f'f15_name{i}',lx,1320,920,240,name,6.8,True,NAVY); text(g,f'f15_amt{i}',lx,1600,920,150,amt,7.2,True,BLUE)
    return pict,151.2


def fig16():
    Wd,H=5650,2050; pict,g=group(16,Wd,H,406.8,147.6); title(g,16,Wd,'三年发展里程碑')
    line(g,'f16_axis',450,1690,5200,1690,BLUE,1.5,True)
    xs=[1150,2825,4500]
    data=[('12 个月',['产品定版 / 一体机交付','金融客户扩展']),('24 个月',['新增行业 / 云订阅收入','并行交付']),('36 个月',['收入规模化 / 复用样板','跨行业复制'])]
    for i,(x,(h,lines_)) in enumerate(zip(xs,data)):
        rect(g,f'f16_box{i}',x-725,650,1450,800,'',WHITE,BORDER,.9,True)
        text(g,f'f16_h{i}',x-625,710,1250,120,h,8.2,True,BLUE); line(g,f'f16_sep{i}',x-500,890,x+500,890,BORDER,.6)
        for j,ln in enumerate(lines_): text(g,f'f16_b{i}_{j}',x-625,1010+j*240,1250,100,ln,4.6,False,TEXT,'center')
        line(g,f'f16_stem{i}',x,1450,x,1650,BLUE,.8); oval(g,f'f16_node{i}',x-45,1645,90,90,WHITE,BLUE,1.2)
    return pict,147.6


BUILD={1:fig1,2:fig2,3:fig3,10:fig10,11:fig11,12:fig12,15:fig15,16:fig16}


def set_para_height(p,hpt):
    pPr=p.find(q(W,'pPr'))
    if pPr is None: pPr=etree.Element(q(W,'pPr')); p.insert(0,pPr)
    sp=pPr.find(q(W,'spacing'))
    if sp is None: sp=etree.SubElement(pPr,q(W,'spacing'))
    sp.set(q(W,'before'),'0'); sp.set(q(W,'after'),'0'); sp.set(q(W,'line'),str(int(round(hpt*20)))); sp.set(q(W,'lineRule'),'exact')
    jc=pPr.find(q(W,'jc'))
    if jc is None: jc=etree.SubElement(pPr,q(W,'jc'))
    jc.set(q(W,'val'),'center')


def patch(src,out):
    src=Path(src); out=Path(out)
    with ZipFile(src) as zin, ZipFile(out,'w',ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data=zin.read(item.filename)
            if item.filename=='word/document.xml':
                root=etree.fromstring(data)
                acs=list(root.xpath('//mc:AlternateContent',namespaces=NS))
                if len(acs)!=8: raise RuntimeError(f'Expected 8 figure alternate contents, got {len(acs)}')
                for ac,fig in zip(acs,[1,2,3,10,11,12,15,16]):
                    p=ac.getparent()
                    while p is not None and p.tag != q(W,'p'): p=p.getparent()
                    if p is None: raise RuntimeError('No paragraph ancestor')
                    pict,h=BUILD[fig](); r=ac.getparent(); idx=r.index(ac); r.remove(ac); r.insert(idx,pict); set_para_height(p,h)
                data=etree.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
            zout.writestr(item,data)


if __name__=='__main__': patch(sys.argv[1],sys.argv[2])
