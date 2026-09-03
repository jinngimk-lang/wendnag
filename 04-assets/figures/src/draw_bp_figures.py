from pathlib import Path
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, FancyArrowPatch
from matplotlib.lines import Line2D

OUT=Path(__file__).resolve().parents[1]; PNG=OUT/'png'; SVG=OUT/'svg'
PNG.mkdir(parents=True,exist_ok=True); SVG.mkdir(parents=True,exist_ok=True)
mpl.rcParams['svg.fonttype']='none'
mpl.rcParams['font.family']='Noto Sans CJK JP'
mpl.rcParams['axes.unicode_minus']=False
NAVY='#17365D'; BLUE='#2F75B5'; PALE='#EAF2F8'; PALE2='#F7FAFD'; BORDER='#A9C4DC'; TEXT='#263645'; MUTED='#68798A'; GRID='#DCE7F0'; WHITE='#FFFFFF'
FIGSIZE={1:(5.65,3.30),2:(5.45,3.45),3:(5.65,3.20),10:(5.65,2.72),11:(5.65,3.25),12:(5.65,3.15),15:(5.65,2.10),16:(5.65,2.05)}

def canvas(n):
    fig=plt.figure(figsize=FIGSIZE[n],dpi=180,facecolor='white'); ax=fig.add_axes([0,0,1,1]); ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis('off'); return fig,ax

def title(ax,s,y=.94,size=18):
    ax.text(.5,y,s,ha='center',va='center',fontsize=size,fontweight='bold',color=NAVY); ax.add_line(Line2D([.46,.54],[y-.052,y-.052],lw=2,color=BLUE))

def box(ax,x,y,w,h,fc=WHITE,ec=BORDER,lw=1,rad=.012):
    p=FancyBboxPatch((x,y),w,h,boxstyle=f'round,pad=0.005,rounding_size={rad}',facecolor=fc,edgecolor=ec,linewidth=lw); ax.add_patch(p); return p

def txt(ax,x,y,s,size=10,weight='normal',color=TEXT,ha='center',va='center',linespacing=1.22):
    ax.text(x,y,s,ha=ha,va=va,fontsize=size,fontweight=weight,color=color,linespacing=linespacing)

def arrow(ax,x1,y1,x2,y2,lw=1.2,c=BLUE):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle='-|>',mutation_scale=10,linewidth=lw,color=c,shrinkA=0,shrinkB=0))

def save(fig,n,slug):
    fig.savefig(SVG/f'fig{n:02d}-{slug}.svg',format='svg',facecolor='white',bbox_inches=None,pad_inches=0)
    fig.savefig(PNG/f'fig{n:02d}-{slug}.png',dpi=360,facecolor='white',bbox_inches=None,pad_inches=0); plt.close(fig)

# Figure 1
fig,ax=canvas(1); title(ax,'三层产品构成同一套企业智能底座')
cols=[(.045,'组织级','AragonTeam','企业 AI 原生\n人机协同工作站','研发团队与组织管理者'),(.365,'通用级','AegisClaw','线上安全通用智能体','跨职能个人与团队'),(.685,'行业级','合约智审 LegalLens','大模型智能体驱动的\n智能合同审核系统','法务、采购、合规与项目管理')]
for x,level,name,desc,aud in cols:
    box(ax,x,.51,.27,.30); txt(ax,x+.135,.765,level,12.2,'bold',NAVY); ax.add_line(Line2D([x+.018,x+.252],[.725,.725],lw=.7,color=BORDER)); txt(ax,x+.135,.665,name,12.2,'bold',NAVY); txt(ax,x+.135,.595,desc,9.4); ax.add_line(Line2D([x+.045,x+.225],[.552,.552],lw=.65,color=BORDER)); txt(ax,x+.135,.525,aud,8.6,color=MUTED); arrow(ax,x+.135,.505,x+.135,.465,1.1)
box(ax,.045,.16,.91,.29,fc=PALE); txt(ax,.50,.412,'统一企业智能底座｜四类企业级要件',13.2,'bold',NAVY)
items=[('身份与权限','智能体是谁\n能碰哪些系统与数据'),('知识与上下文','企业知识与项目背景\n可被稳定调用'),('流程与状态','任务有依赖、有状态\n可回退、可重入'),('审计与留痕','谁做、何时做、依据什么\n全程可查询')]
for i,(h,b) in enumerate(items):
    x=.064+i*.224; box(ax,x,.205,.205,.135,fc=WHITE,rad=.009); txt(ax,x+.1025,.302,h,9.5,'bold',NAVY); txt(ax,x+.1025,.248,b,7.8)
txt(ax,.5,.075,'组织级提供约束与留痕｜通用级提供安全执行力｜行业级提供领域深度',8.6,'bold',NAVY); save(fig,1,'three-layer-enterprise-intelligence-base')

# Figure 2
fig,ax=canvas(2); title(ax,'企业级 Agentic AI 市场规模')
plot=ax.inset_axes([.14,.18,.75,.66]); vals=[67.6,460.4]; xs=[0,1]
plot.bar(xs,vals,width=.34,color=[PALE,'#D9E8F7'],edgecolor=BLUE,linewidth=1.2); plot.set_ylim(0,530); plot.set_xlim(-.42,1.42); plot.set_xticks(xs,['2025 年','2030 年（预测）']); plot.tick_params(axis='x',labelsize=10,colors=NAVY); plot.tick_params(axis='y',labelsize=8.5,colors=NAVY); plot.set_ylabel('市场规模（亿美元）',fontsize=9.5,color=NAVY,labelpad=8); plot.grid(axis='y',color=GRID,linewidth=.55); plot.set_axisbelow(True); plot.spines[['top','right']].set_visible(False); plot.spines[['left','bottom']].set_color(BLUE)
plot.text(0,82,'67.6',ha='center',fontsize=11.5,fontweight='bold',color=NAVY); plot.text(1,477,'460.4',ha='center',fontsize=11.5,fontweight='bold',color=NAVY); plot.annotate('CAGR\n47%',xy=(1,455),xytext=(.45,290),fontsize=10.5,fontweight='bold',ha='center',va='center',color=NAVY,bbox=dict(boxstyle='round,pad=.45',fc=WHITE,ec=BLUE,lw=1),arrowprops=dict(arrowstyle='-|>',lw=1,color=BLUE)); txt(ax,.5,.075,'数据来源：MarketsandMarkets｜按原 BP 口径',8.5,color=MUTED); save(fig,2,'enterprise-agentic-ai-market')

# Figure 3
fig,ax=canvas(3); title(ax,'企业 AI 能力四级阶梯')
steps=[('L1','对话问答','回答问题','停在个人对话'),('L2','助手辅助','补全与草拟','仍需人工搬运'),('L3','智能体执行','执行多步任务','缺身份 / 权限边界'),('L4','组织智能','组织级协同','进入权限与流程')]
xs=[.055,.285,.515,.745]; ys=[.40,.46,.52,.58]
for i,((lv,h,a,b),x,y) in enumerate(zip(steps,xs,ys)):
    ax.add_patch(Rectangle((x-.008,.34),.19,y-.34,facecolor='#F1F6FB',edgecolor='none',zorder=0)); box(ax,x,y,.185,.205,rad=.010); txt(ax,x+.0925,y+.155,f'{lv}  {h}',11.5,'bold',NAVY); ax.add_line(Line2D([x+.02,x+.165],[y+.116,y+.116],lw=.65,color=BORDER)); txt(ax,x+.0925,y+.075,a,9.7,'bold'); txt(ax,x+.0925,y+.038,b,8.8,color=MUTED)
    if i<3: arrow(ax,x+.185,y+.10,xs[i+1],ys[i+1]+.10,1.0)
txt(ax,.5,.285,'每上一阶需补齐的四类企业级要件',10.2,'bold',NAVY)
for i,r in enumerate(['身份与权限','知识与上下文','流程与状态','审计与留痕']):
    x=.065+i*.225; box(ax,x,.175,.195,.075,fc=PALE,rad=.008); txt(ax,x+.0975,.2125,r,9.6,'bold',NAVY)
txt(ax,.5,.075,'前三阶描述“单个智能体能做什么”；L4 描述“组织如何让智能体进入生产流程”',8.6,'bold',NAVY); save(fig,3,'enterprise-ai-four-level-ladder')

# Figure 10
fig,ax=canvas(10); title(ax,'公司层面的三种交付形态')
cards=[('I  私有化服务器部署','数据、模型、知识与执行\n全部在企业内网闭环','对接现有身份、权限与审计体系','适用：总部级客户'),('II  便携式一体机','本地模型 + AI 算力 + 协作平台\n开箱即用，支持断网运行','面向现场化、临时化部署','适用：项目现场 / 无外网'),('III  私有云服务','私有网络内提供模型、算力\n与协作平台完整能力','兼顾集中管理与私有网络边界','适用：公司与团队办公')]
for i,(h,b,m,f) in enumerate(cards):
    x=.035+i*.322; box(ax,x,.26,.287,.55); txt(ax,x+.1435,.752,h,11.3,'bold',NAVY); ax.add_line(Line2D([x+.02,x+.267],[.705,.705],lw=.7,color=BORDER)); txt(ax,x+.1435,.575,b,8.6,'bold'); txt(ax,x+.1435,.475,m,7.7,color=MUTED); box(ax,x+.025,.305,.237,.095,fc=PALE,rad=.008); txt(ax,x+.1435,.3525,f,8.0,'bold',NAVY)
txt(ax,.5,.115,'通用级 AegisClaw 以线上云端工作空间提供；行业级合约智审采用公有云与私有化双形态',8.2,'bold',NAVY); save(fig,10,'three-delivery-models')

# Figure 11
fig,ax=canvas(11); title(ax,'合约智审系统四层架构')
layers=[('应用层',['智能审查','上下游一致性','资信审查','文稿智审','合同生成','知识库']),('核心服务层',['文档解析','知识抽取','知识图谱','规则引擎','多智能体协同','垂直大模型']),('技术架构层',['前端框架','后端服务','存储与检索','部署与运维']),('基础层',['算力资源','存储资源'])]; ys=[.70,.51,.32,.13]
for idx,((lname,items),y) in enumerate(zip(layers,ys)):
    box(ax,.035,y,.93,.14,fc=PALE if idx%2==0 else WHITE,rad=.008); txt(ax,.12,y+.07,lname,11.8,'bold',NAVY); ax.add_line(Line2D([.195,.195],[y+.025,y+.115],lw=.7,color=BORDER)); n=len(items); x0=.22; total=.72; gap=.009; iw=(total-gap*(n-1))/n
    for j,it in enumerate(items):
        x=x0+j*(iw+gap); box(ax,x,y+.036,iw,.068,rad=.005); txt(ax,x+iw/2,y+.07,it,7.7,'bold' if idx<2 else 'normal')
    if idx<3: arrow(ax,.5,y-.002,.5,ys[idx+1]+.142,.9)
txt(ax,.5,.055,'基础资源 → 技术架构 → 核心服务 → 应用能力，四层职责清晰解耦',8.2,color=MUTED); save(fig,11,'legallens-four-layer-architecture')

# Figure 12
fig,ax=canvas(12); title(ax,'收入结构与客户复制路径')
txt(ax,.16,.84,'四条收入线',11.6,'bold',NAVY); txt(ax,.84,.84,'三条复制路径',11.6,'bold',NAVY)
left=['私有化部署软件授权','便携式一体机','云服务订阅','行业实施与规则库共建\n及年度运维']
for i,s in enumerate(left):
    y=.69-i*.13; box(ax,.035,y,.255,.095,rad=.007); txt(ax,.1625,y+.0475,s,8.8,'bold'); arrow(ax,.29,y+.0475,.395,.49,.9)
box(ax,.395,.31,.22,.36,fc=PALE,rad=.009); txt(ax,.505,.605,'标准化实施方法',11.2,'bold',NAVY); ax.add_line(Line2D([.425,.585],[.565,.565],lw=.7,color=BORDER)); txt(ax,.505,.455,'首单共建行业规则库\n与统一审查口径',8.4,'bold'); txt(ax,.505,.365,'规则、模板、图谱\n沉淀为领域资产',8.0)
right=[('战略渠道复制','省公司继承已验证口径'),('行业样板复制','通信、交通形成量化样板'),('政企触点','技术评审与试点立项触点')]
for i,(h,b) in enumerate(right):
    y=.65-i*.16; box(ax,.705,y,.25,.115,rad=.007); txt(ax,.83,y+.078,h,9.1,'bold',NAVY); txt(ax,.83,y+.034,b,7.6); arrow(ax,.615,.49,.705,y+.058,.9)
txt(ax,.5,.11,'同一行业第 N 个客户不必从零起步：实施投入随渗透率下降，毛利率随之改善',8.5,'bold',NAVY); save(fig,12,'revenue-and-customer-replication')

# Figure 15
fig,ax=canvas(15); title(ax,'融资资金用途结构（合计 1000 万元）',.90,16.5)
segments=[(.40,'40%','产品研发与\n技术攻关','400 万元'),(.20,'20%','市场与\n渠道建设','200 万元'),(.20,'20%','交付与\n实施团队','200 万元'),(.12,'12%','一体机产品化\n与备货','120 万元'),(.08,'8%','运营储备','80 万元')]
x=.04; y=.57; totalw=.92; h=.17
for i,(p,pct,name,amt) in enumerate(segments):
    w=totalw*p; ax.add_patch(Rectangle((x,y),w,h,facecolor='#DCEBF7' if i==0 else PALE,edgecolor=BLUE,linewidth=.8)); txt(ax,x+w/2,y+h/2,pct,11.3,'bold',NAVY); x+=w
for (p,pct,name,amt),cx in zip(segments,[.13,.315,.50,.685,.87]):
    txt(ax,cx,.365,name,7.9,'bold',NAVY); txt(ax,cx,.235,amt,8.3,'bold',BLUE)
save(fig,15,'funding-use-structure')

# Figure 16
fig,ax=canvas(16); title(ax,'三年发展里程碑',.90,16.5); ax.add_line(Line2D([.07,.94],[.22,.22],lw=1.4,color=BLUE)); arrow(ax,.94,.22,.97,.22,1.4)
xs=[.23,.50,.77]; content=[('12 个月',['三层产品商业化版本定版','一体机产品化并完成首批交付','金融行业第二家客户私有化落地']),('24 个月',['规则库覆盖新增两个行业','云订阅形成经常性收入','实施团队支撑并行项目']),('36 个月',['四条收入线全部形成规模','四个行业各建可复用样板','具备向新行业标准化复制能力'])]
for x,(h,lines) in zip(xs,content):
    ax.add_patch(Circle((x,.22),.013,facecolor=WHITE,edgecolor=BLUE,linewidth=1.2)); ax.add_line(Line2D([x,x],[.233,.34],lw=.8,color=BLUE)); box(ax,x-.155,.34,.31,.42,rad=.008); txt(ax,x,.69,h,12.5,'bold',BLUE); ax.add_line(Line2D([x-.11,x+.11],[.625,.625],lw=.65,color=BORDER))
    for j,line in enumerate(lines): txt(ax,x,.54-j*.08,line,8.4)
txt(ax,.5,.075,'每档里程碑均以客户、产品形态和行业覆盖等可验证结果作为完成标志',8.1,'bold',NAVY); save(fig,16,'three-year-milestones')

print('generated',len(list(SVG.glob('*.svg'))),'SVG and',len(list(PNG.glob('*.png'))),'PNG')
