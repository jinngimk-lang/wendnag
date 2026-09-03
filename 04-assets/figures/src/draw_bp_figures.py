from pathlib import Path
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, FancyArrowPatch
from matplotlib.lines import Line2D

OUT = Path(__file__).resolve().parents[1]
PNG = OUT / 'png'
SVG = OUT / 'svg'
PNG.mkdir(parents=True, exist_ok=True)
SVG.mkdir(parents=True, exist_ok=True)

FONT = 'Noto Sans CJK JP'
NAVY = '#102A56'
BLUE = '#2F6FDB'
PALE = '#EEF5FF'
PALE2 = '#F7FAFF'
BORDER = '#A8C6F2'
TEXT = '#1E2B3A'
MUTED = '#5F6F82'
GRID = '#DDE8F6'
WHITE = '#FFFFFF'

mpl.rcParams['font.family'] = FONT
mpl.rcParams['axes.unicode_minus'] = False

SIZES = {
    1:(1597,879), 2:(1180,920), 3:(1597,818), 10:(1597,725),
    11:(1597,910), 12:(1597,818), 15:(1358,502), 16:(1597,510)
}

def canvas(num):
    w,h=SIZES[num]
    dpi=220
    fig=plt.figure(figsize=(w/dpi,h/dpi), dpi=dpi, facecolor='white')
    ax=fig.add_axes([0,0,1,1]); ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis('off')
    return fig, ax

def title(ax, text, y=0.94, size=22):
    ax.text(0.5,y,text,ha='center',va='center',fontsize=size,fontweight='bold',color=NAVY)
    ax.add_line(Line2D([0.44,0.56],[y-0.055,y-0.055],lw=2,color=BLUE))

def box(ax,x,y,w,h,fc=PALE2,ec=BORDER,lw=1.2,rad=0.012):
    p=FancyBboxPatch((x,y),w,h,boxstyle=f'round,pad=0.006,rounding_size={rad}',
                     facecolor=fc,edgecolor=ec,linewidth=lw)
    ax.add_patch(p); return p

def txt(ax,x,y,s,size=11,weight='normal',color=TEXT,ha='center',va='center'):
    ax.text(x,y,s,fontsize=size,fontweight=weight,color=color,ha=ha,va=va,linespacing=1.35)

def dot(ax,x,y,r=0.008,c=BLUE):
    ax.add_patch(Circle((x,y),r,facecolor=c,edgecolor=c))

def arrow(ax,x1,y1,x2,y2,c=BLUE,lw=1.6,style='-|>'):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle=style,mutation_scale=13,
                                 linewidth=lw,color=c,shrinkA=0,shrinkB=0))

def save(fig,num,slug):
    # PNG is exported at 2x the original pixel dimensions for Word projection use.
    # SVG is retained as the infinitely scalable source of truth.
    fig.savefig(PNG/f'fig{num:02d}-{slug}.png',dpi=440,bbox_inches=None,pad_inches=0,facecolor='white')
    fig.savefig(SVG/f'fig{num:02d}-{slug}.svg',format='svg',bbox_inches=None,pad_inches=0,facecolor='white')
    plt.close(fig)

# FIG 1
fig,ax=canvas(1); title(ax,'三层产品构成同一套企业智能底座',0.94,22)
cols=[(0.055,'组织级','AragonTeam','企业 AI 原生\n人机协同工作站','研发团队与\n组织管理者'),
      (0.365,'通用级','AegisClaw\n（曾用名 InkClaw）','线上安全\n通用智能体','跨职能个人\n与团队'),
      (0.675,'行业级','合约智审 LegalLens','大模型智能体驱动的\n智能合同审核系统','法务、采购、\n合规与项目管理')]
for x,level,name,desc,aud in cols:
    box(ax,x,0.49,0.27,0.34,fc=WHITE)
    txt(ax,x+0.135,0.785,level,15,'bold',NAVY)
    ax.add_line(Line2D([x+0.02,x+0.25],[0.75,0.75],lw=0.8,color=BORDER))
    if '曾用名' in name:
        txt(ax,x+0.135,0.705,'AegisClaw',14,'bold',NAVY)
        txt(ax,x+0.135,0.665,'（曾用名 InkClaw）',9.2,'normal',MUTED)
        txt(ax,x+0.135,0.595,desc,10.2)
        ax.add_line(Line2D([x+0.05,x+0.22],[0.555,0.555],lw=0.7,color=BORDER))
        txt(ax,x+0.135,0.515,aud,9.2)
    else:
        txt(ax,x+0.135,0.69,name,14,'bold',NAVY)
        txt(ax,x+0.135,0.61,desc,10.2)
        ax.add_line(Line2D([x+0.05,x+0.22],[0.565,0.565],lw=0.7,color=BORDER))
        txt(ax,x+0.135,0.52,aud,9.2)
    arrow(ax,x+0.135,0.485,x+0.135,0.445,lw=1.3)
box(ax,0.055,0.15,0.89,0.28,fc=PALE)
txt(ax,0.5,0.39,'统一企业智能底座｜四类企业级要件',17,'bold',NAVY)
items=[('身份与权限','智能体是谁，\n能碰哪些系统与数据'),('知识与上下文','企业知识与项目背景\n可被稳定调用'),('流程与状态','任务有依赖、有状态、\n可回退、可重入'),('审计与留痕','谁做的、何时做的、\n依据是什么全可查')]
for i,(a,b) in enumerate(items):
    x=0.075+i*0.22
    box(ax,x,0.205,0.20,0.13,fc=WHITE,rad=0.01)
    txt(ax,x+0.10,0.300,a,11.2,'bold',NAVY)
    txt(ax,x+0.10,0.242,b,8.7)
txt(ax,0.5,0.085,'能力在三层之间流动：组织级提供约束与留痕，通用级提供安全执行力，行业级提供领域深度',10.5,'bold',NAVY)
save(fig,1,'three-layer-enterprise-intelligence-base')

# FIG 2
fig,ax=canvas(2); title(ax,'企业级 Agentic AI 市场规模',0.95,22)
plot=ax.inset_axes([0.13,0.16,0.78,0.67]); plot.set_facecolor('white')
vals=[67.6,460.4]; xs=[0,1]
plot.bar(xs,vals,width=0.34,color=[PALE, '#DDEBFF'],edgecolor=BLUE,linewidth=1.4)
plot.set_ylim(0,540); plot.set_xlim(-0.35,1.35)
plot.set_xticks(xs,['2025 年','2030 年（预测）'],fontsize=12,color=NAVY)
plot.set_ylabel('市场规模（亿美元）',fontsize=11,color=NAVY,labelpad=10)
plot.tick_params(axis='y',labelsize=10,colors=NAVY)
plot.grid(axis='y',color=GRID,linewidth=0.7,alpha=0.7); plot.set_axisbelow(True)
plot.spines[['top','right']].set_visible(False); plot.spines[['left','bottom']].set_color(BLUE)
plot.text(0,78,'67.6',ha='center',va='bottom',fontsize=14,fontweight='bold',color=NAVY)
plot.text(1,472,'460.4',ha='center',va='bottom',fontsize=14,fontweight='bold',color=NAVY)
plot.annotate('年复合增长率\n47%',xy=(1,455),xytext=(0.50,285),ha='center',va='center',fontsize=13,fontweight='bold',color=NAVY,
              bbox=dict(boxstyle='round,pad=0.55',fc=WHITE,ec=BLUE,lw=1.2),arrowprops=dict(arrowstyle='-|>',color=BLUE,lw=1.3))
txt(ax,0.5,0.075,'数据来源：MarketsandMarkets（按原 BP 口径）',10.5,color=MUTED)
save(fig,2,'enterprise-agentic-ai-market')

# FIG 3
fig,ax=canvas(3); title(ax,'企业 AI 能力四级阶梯',0.94,22)
steps=[(0.035,0.18,'L1  对话问答','会回答问题\n产出停在个人聊天框'),(0.205,0.28,'L2  助手辅助','会补全、会草拟\n输出需人工二次搬运'),(0.375,0.39,'L3  智能体执行','能完成多步任务\n缺企业身份与权限边界'),(0.545,0.51,'L4  组织智能','人与智能体在同一套\n权限与流程中协同')]
for i,(x,y,h1,h2) in enumerate(steps):
    box(ax,x,y,0.15,0.20,fc=WHITE); txt(ax,x+0.075,y+0.135,h1,12,'bold',NAVY)
    ax.add_line(Line2D([x+0.02,x+0.13],[y+0.10,y+0.10],lw=0.8,color=BORDER)); txt(ax,x+0.075,y+0.055,h2,9.5)
    if i<3: arrow(ax,x+0.15,y+0.10,steps[i+1][0],steps[i+1][1]+0.10,lw=1.2)
box(ax,0.735,0.18,0.235,0.62,fc=PALE); txt(ax,0.852,0.745,'每上一阶需补齐的\n四类企业级要件',15,'bold',NAVY)
for i,s in enumerate(['身份与权限','知识与上下文','流程与状态','审计与留痕']):
    y=0.62-i*0.105; box(ax,0.755,y,0.195,0.075,fc=WHITE,rad=0.008); txt(ax,0.852,y+0.037,s,11.5,'bold',TEXT)
txt(ax,0.5,0.09,'前三级描述单个智能体能做到什么，第四级描述组织能做到什么。公司产品处在 L4',10.5,'bold',NAVY)
save(fig,3,'enterprise-ai-four-level-ladder')

# FIG 10
fig,ax=canvas(10); title(ax,'公司层面的三种交付形态',0.94,22)
cards=[('I  私有化服务器部署','数据不出企业网，模型、知识\n与执行全部内网闭环；对接企业\n现有身份、权限与审计体系','适用：有机房与运维能力的\n总部级客户'),('II  便携式一体机','本地模型、AI 算力与协作平台\n三合一，开箱即用；断网环境下\n仍可运行完整协同流程','适用：项目现场、临时团队、\n无外网场景'),('III  私有云服务','私有网络模型、AI 算力与协作\n平台三合一，开箱即用；私有\n网络环境下完整可用','适用：公司与团队办公场地')]
for i,(h,b,f) in enumerate(cards):
    x=0.04+i*0.32; box(ax,x,0.25,0.28,0.58,fc=WHITE); txt(ax,x+0.14,0.75,h,15,'bold',NAVY)
    ax.add_line(Line2D([x+0.02,x+0.26],[0.70,0.70],lw=0.8,color=BORDER)); txt(ax,x+0.14,0.505,b,9.6)
    box(ax,x+0.02,0.285,0.24,0.115,fc=PALE,rad=0.008); txt(ax,x+0.14,0.342,f,9.1,'bold',NAVY)
txt(ax,0.5,0.115,'产品层面另有差异：通用级 AegisClaw（曾用名 InkClaw）以线上云端工作空间提供；\n行业级合约智审为公有云与私有化双形态并行',8.6,'bold',NAVY)
save(fig,10,'three-delivery-models')

# FIG 11
fig,ax=canvas(11); title(ax,'合约智审系统四层架构',0.95,22)
layers=[('应用层',['智能审查','上下游一致性','资信审查','文稿智审','合同生成','知识库']),('核心服务层',['文档解析','知识抽取','知识图谱','规则引擎','多智能体协同','垂直大模型']),('技术架构层',['前端框架','后端服务','存储与检索','部署与运维']),('基础层',['算力资源','存储资源'])]
ys=[0.70,0.51,0.32,0.14]
for idx,((lname,items),y) in enumerate(zip(layers,ys)):
    box(ax,0.045,y,0.91,0.14,fc=PALE if idx%2==0 else WHITE,rad=0.008); txt(ax,0.13,y+0.07,lname,14,'bold',NAVY)
    ax.add_line(Line2D([0.205,0.205],[y+0.02,y+0.12],lw=0.8,color=BORDER)); n=len(items); x0=0.23; total=0.70; gap=0.012; iw=(total-gap*(n-1))/n
    for j,it in enumerate(items):
        x=x0+j*(iw+gap); box(ax,x,y+0.035,iw,0.07,fc=WHITE,rad=0.006); txt(ax,x+iw/2,y+0.07,it,9.5,'bold' if idx<2 else 'normal')
    if idx<3: arrow(ax,0.5,y-0.005,0.5,ys[idx+1]+0.145,lw=1.1)
txt(ax,0.5,0.055,'基础层提供算力和存储保障；技术架构层整合前后端与存储部署技术；核心服务层聚合解析、处理和智能模型能力；应用层覆盖智能审查、合同与资信等功能',8.9,color=MUTED)
save(fig,11,'legallens-four-layer-architecture')

# FIG 12
fig,ax=canvas(12); title(ax,'收入结构与客户复制路径',0.95,22)
txt(ax,0.17,0.84,'四条收入线',15,'bold',NAVY); txt(ax,0.82,0.84,'三条复制路径',15,'bold',NAVY)
left=['私有化部署软件授权','便携式一体机','云服务订阅','行业实施与规则库共建\n及年度运维']
for i,s in enumerate(left):
    y=0.69-i*0.13; box(ax,0.045,y,0.25,0.095,fc=WHITE,rad=0.007); txt(ax,0.17,y+0.048,s,10.5,'bold'); arrow(ax,0.295,y+0.048,0.39,0.49,lw=1.0)
box(ax,0.39,0.31,0.23,0.36,fc=PALE,rad=0.008); txt(ax,0.505,0.605,'标准化实施方法',13.5,'bold',NAVY)
ax.add_line(Line2D([0.425,0.585],[0.565,0.565],lw=0.8,color=BORDER)); txt(ax,0.505,0.435,'行业首单与客户共建\n规则库与审查口径；\n规则、模板与图谱沉淀为领域资产\n交付一次，能力厚一层',9.1)
right=[('战略渠道复制','中通服体系内省公司\n直接继承已验证口径'),('行业样板复制','通信与交通已量化样板；\n法律与金融私有化落地'),('政企触点','高校成果转化背景带来\n技术评审与试点立项触点')]
for i,(h,b) in enumerate(right):
    y=0.65-i*0.16; box(ax,0.70,y,0.255,0.115,fc=WHITE,rad=0.007)
    txt(ax,0.827,y+0.090,h,10.0,'bold',NAVY); ax.add_line(Line2D([0.73,0.925],[y+0.063,y+0.063],lw=0.6,color=BORDER)); txt(ax,0.827,y+0.025,b,7.8); arrow(ax,0.62,0.49,0.70,y+0.058,lw=1.0)
txt(ax,0.5,0.12,'同一行业的第 N 个客户不必从零起步，实施投入随渗透率下降，毛利率随之改善',10.5,'bold',NAVY)
save(fig,12,'revenue-and-customer-replication')

# FIG 15
fig,ax=canvas(15); title(ax,'融资资金用途结构（合计 1000 万元）',0.92,20)
segments=[(0.40,'40%','产品研发与\n技术攻关','400 万元'),(0.20,'20%','市场与\n渠道建设','200 万元'),(0.20,'20%','交付与\n实施团队','200 万元'),(0.12,'12%','一体机产品化\n与备货','120 万元'),(0.08,'8%','运营储备','80 万元')]
x=0.045; y=0.50; totalw=0.91; h=0.19; centers=[]
for i,(p,pct,name,amt) in enumerate(segments):
    w=totalw*p; rect=Rectangle((x,y),w,h,facecolor=PALE if i>0 else '#DCEBFF',edgecolor=BLUE,linewidth=1.0)
    ax.add_patch(rect); txt(ax,x+w/2,y+h/2,pct,16,'bold',NAVY); centers.append(x+w/2); x+=w
label_x=[centers[0],centers[1],centers[2],centers[3]-0.025,centers[4]+0.025]; name_sizes=[9.2,9.2,9.2,8.0,8.0]
for i,((p,pct,name,amt),cx,lx) in enumerate(zip(segments,centers,label_x)):
    ax.add_line(Line2D([cx,cx],[y,0.405],lw=0.8,color=BLUE)); dot(ax,cx,0.405,0.0045)
    if lx!=cx: ax.add_line(Line2D([cx,lx],[0.405,0.37],lw=0.7,color=BLUE))
    txt(ax,lx,0.285,name,name_sizes[i],'bold',NAVY); txt(ax,lx,0.185,amt,9.2,'bold',BLUE)
save(fig,15,'funding-use-structure')

# FIG 16
fig,ax=canvas(16); title(ax,'三年发展里程碑',0.91,20)
ax.add_line(Line2D([0.07,0.94],[0.23,0.23],lw=1.7,color=BLUE)); arrow(ax,0.94,0.23,0.97,0.23,lw=1.7)
xs=[0.25,0.50,0.75]
content=[('12 个月',['三层产品商业化版本定版','一体机完成产品化并首批交付','金融行业第二家客户私有化落地']),('24 个月',['规则库覆盖新增两个行业','云订阅形成经常性收入','实施团队支撑并行项目']),('36 个月',['四条收入线全部形成规模','四个行业各建可复用样板','具备向新行业标准化复制的能力'])]
for x,(h,lines) in zip(xs,content):
    dot(ax,x,0.23,0.012,WHITE); ax.add_patch(Circle((x,0.23),0.015,fill=False,edgecolor=BLUE,linewidth=1.5)); ax.add_line(Line2D([x,x],[0.245,0.35],lw=1.0,color=BLUE))
    box(ax,x-0.16,0.35,0.32,0.40,fc=WHITE,rad=0.008); txt(ax,x,0.68,h,16,'bold',BLUE); ax.add_line(Line2D([x-0.12,x+0.12],[0.62,0.62],lw=0.8,color=BORDER))
    for j,line in enumerate(lines): txt(ax,x,0.54-j*0.075,line,10.5)
txt(ax,0.5,0.095,'每一档里程碑的完成标志均可用客户数、产品形态与行业覆盖验证',10,'bold',NAVY)
save(fig,16,'three-year-milestones')

print('Generated 8 PNG + 8 SVG figures.')
