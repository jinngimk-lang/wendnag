// AragonTeam editable Figma project screen builder
// Local development plugin: execute while the target Figma file is open.
// All interface elements are native editable Figma nodes; SVG icons become vectors.
// Interactions: home -> project detail / kanban / members overlay / create overlay.
(async () => {
  const S = {
    navy: '#111D63', blue: '#536FAA', coral: '#FF4A1B', blueDeep: '#2452AA',
    pale: '#FFF1EC', gray: '#F6F7FA', white: '#FFFFFF', border: '#EBEEF5',
    muted: '#6B82B6', bg: '#FCFDFE', sky: '#E5F3FF', label: '#FFF2EE'
  };
  const rgba = (hex) => {
    const v = hex.replace('#','');
    return {r:parseInt(v.slice(0,2),16)/255,g:parseInt(v.slice(2,4),16)/255,b:parseInt(v.slice(4,6),16)/255};
  };
  const solid = (hex) => [{type:'SOLID',color:rgba(hex)}];
  const created = [];
  function rect(parent, name, x,y,w,h, fill, radius=0, stroke) {
    const n=figma.createFrame(); n.name=name;
    parent.appendChild(n); n.x=x;n.y=y;n.resize(w,h);n.cornerRadius=radius;
    n.fills=fill?solid(fill):[]; n.strokes=stroke?solid(stroke):[];
    n.strokeWeight=stroke?1:0; n.clipsContent=false;
    created.push(n.id);return n;
  }
  function ellipse(parent,name,x,y,w,h,fill) {
    const n=figma.createEllipse(); parent.appendChild(n);n.name=name;n.x=x;n.y=y;n.resize(w,h);n.fills=solid(fill);created.push(n.id);return n;
  }
  function svg(parent,name,x,y,size,path,color=S.blue) {
    try {
      const markup=`<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="${color}" stroke-width="1.85" stroke-linecap="round" stroke-linejoin="round">${path}</svg>`;
      const n=figma.createNodeFromSvg(markup); parent.appendChild(n);
      n.name=name;n.x=x;n.y=y;n.resize(size,size); created.push(n.id);return n;
    } catch(e){return rect(parent,name+' icon fallback',x,y,size,size, S.gray,3);}
  }
  const glyphs = {
    chat:'<path d="M20 11.6a8.3 8.3 0 0 1-11.8 7.5L3 20l1.2-4.5A8.4 8.4 0 1 1 20 11.6z"/><circle cx="8" cy="12" r=".7" fill="currentColor"/><circle cx="12" cy="12" r=".7"/><circle cx="16" cy="12" r=".7"/>',
    folder:'<path d="M3 6v14h18V9H12L9 6z"/>',
    people:'<circle cx="9" cy="8" r="3.5"/><path d="M2 21v-2a7 7 0 0 1 14 0v2zM17 5a3 3 0 0 1 0 6M18 15a5 5 0 0 1 4 5"/>',
    user:'<circle cx="12" cy="7" r="4"/><path d="M4 22v-2a8 8 0 0 1 16 0v2"/>',
    settings:'<path d="M10 2h4l.6 2.5 2.3 1L19 4l2.8 2.9-1.5 2.2 1 2.3L24 12v3l-2.7.5-1 2.3 1.5 2.2L19 23l-2.1-1.5-2.3 1L14 25h-4l-.6-2.5-2.3-1L5 23l-2.8-3 1.5-2.2-1-2.3L0 15v-3l2.7-.6 1-2.3L2.2 7 5 4l2.1 1.5 2.3-1z" transform="translate(1 -2) scale(.9)"/><circle cx="12" cy="12" r="3"/>',
    grid:'<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>',
    board:'<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M8 8v8m4-11v12m5-8v8"/>',
    page:'<path d="M6 2h9l5 5v15H5V2zM15 2v5h5M9 12h7M9 16h7"/>',
    code:'<path d="m9 6-6 6 6 6M15 6l6 6-6 6m-2-15-3 18"/>',
    bulb:'<path d="M9 19h6m-5 3h4M8 15a7 7 0 1 1 8 0l-1 3H9Z"/>',
    layers:'<path d="m12 2 10 6-10 6L2 8Zm-10 11 10 6 10-6M2 18l10 5 10-5"/>',
    search:'<circle cx="11" cy="11" r="7"/><path d="m16 16 5 5"/>',
    sun:'<circle cx="12" cy="12" r="4"/><path d="M12 1v4m0 14v4M1 12h4m14 0h4M4 4l3 3m10 10 3 3M20 4l-3 3M7 17l-3 3"/>',
    bell:'<path d="M5 18h14c-2-2-2-4-2-7a5 5 0 0 0-10 0c0 3 0 5-2 7ZM10 21h4"/>',
    plus:'<circle cx="12" cy="12" r="10"/><path d="M12 6v12M6 12h12"/>',
    external:'<path d="M14 4h6v6m0-6-9 9M20 14v6H4V4h6"/>',
    more:'<circle cx="12" cy="5" r="2" fill="currentColor" stroke="none"/><circle cx="12" cy="12" r="2" fill="currentColor" stroke="none"/><circle cx="12" cy="19" r="2" fill="currentColor" stroke="none"/>',
    chevron:'<path d="m5 9 7 7 7-7"/>',
  };
  const fonts=await figma.listAvailableFontsAsync();
  const found=(family,style)=>fonts.some(f=>f.fontName.family===family && f.fontName.style===style);
  let family=['PingFang SC','Noto Sans SC','Microsoft YaHei','Inter'].find(x=>found(x,'Regular')) || 'Inter';
  const regular={family,style:'Regular'};
  const boldStyle=['SemiBold','Semi Bold','Bold','Medium'].find(x=>found(family,x))||'Regular';
  const bold={family,style:boldStyle};
  await Promise.all([figma.loadFontAsync(regular),figma.loadFontAsync(bold)]);
  function t(parent,name,chars,x,y,w,fontSize=16,color=S.navy,isBold=false){
    const n=figma.createText(); parent.appendChild(n);n.name=name;
    n.fontName=isBold?bold:regular; n.fontSize=fontSize; n.fills=solid(color);
    n.characters=chars; n.textAutoResize='HEIGHT';n.resize(w,Math.max(fontSize*1.5,22));
    n.x=x;n.y=y;created.push(n.id);return n;
  }
  function line(parent,name,x,y,w,color=S.border){rect(parent,name,x,y,w,1,color);}
  function button(parent,name,label,x,y,w,h,fill,color,iconName){
    const f=rect(parent,name,x,y,w,h,fill,9);
    if(iconName)svg(f,`icon / ${iconName}`,Math.max(14,(w-(label.length*16+33))/2),Math.round((h-18)/2),18,glyphs[iconName],color);
    const tx=iconName?Math.max(38,(w-(label.length*16+33))/2+27):Math.max(8,(w-label.length*16)/2);
    t(f,`text / ${label}`,label,tx,(h-22)/2,w-tx-5,15,color,true);
    return f;
  }
  let linked=0; const linkErrors=[];
  async function link(node,target,nav='NAVIGATE'){
    const action={type:'NODE',destinationId:target.id,navigation:nav,transition:null};
    try {await node.setReactionsAsync([{trigger:{type:'ON_CLICK'},actions:[action]}]);linked++;}
    catch (e) {linkErrors.push(node.name + ': ' + String(e&&e.message||e));}
  }
  const homePage=figma.currentPage;
  let maxX=0;for(const n of homePage.children){if('x' in n && 'width' in n)maxX=Math.max(maxX,n.x+n.width);}
  const startX=maxX+160;
  function screen(name,x){const f=rect(homePage,name,x,0,1664,913,S.bg);f.clipsContent=true;return f;}
  const home=screen('01 / 项目管理 · 主页面（原生可编辑）',startX);
  const detail=screen('02 / AragonTeam Platform · 项目详情',startX+1890);
  const board=screen('03 / 需求看板 · 交互目标',startX+3780);
  const createOverlay=rect(homePage,'04 / 新建项目 · 原型弹窗',startX+5670,100,480,490,S.white,16,S.border);
  const memberOverlay=rect(homePage,'05 / 项目成员 · 原型弹窗',startX+5670,700,480,415,S.white,16,S.border);
  const menuTargets=[], openTargets=[], memberTargets=[];
  function appChrome(s,selected='项目',sideSelected='项目管理',caption='项目',subtitle='研发项目管理'){
    rect(s,'左侧主导航 / 白色底板',0,0,70,913,S.white);line(s,'主导航分隔线',69,0,1,'#E5E9F1');
    rect(s,'品牌图标',18,14,32,32,S.coral,10);ellipse(s,'品牌留白圆形',27,22,14,14,S.white);
    const rails=[['chat','智能体',92],['folder','项目',172],['people','团队',245],['user','个人',318],['settings','设置',866]];
    for(const [ic,title,y] of rails){if(title===selected)rect(s,`一级导航 / ${title}（选中）`,6,y-22,56,55,S.pale,12);const node=svg(s,`一级导航图标 / ${title}`,20,y-14,28,glyphs[ic],title===selected?S.coral:'#4B629C'); if(title==='项目')menuTargets.push(node);}
    rect(s,'二级侧边栏 / 底板',70,0,246,913,S.white);line(s,'二级导航分隔线',315,0,1,'#E5E9F1');
    t(s,'二级标题',caption,92,9,170,23,S.navy,true);
    const subs=[['grid','项目管理'],['board','需求看板'],['board','BUG看板'],['page','文档'],['code','代码仓'],['bulb','建议'],['layers','版本']];
    subs.forEach(([ic,title],i)=>{
      const y=52+i*60;
      if(title===sideSelected)rect(s,`二级导航选中态 / ${title}`,80,y,224,52,S.pale,9);
      const it=svg(s,`二级导航图标 / ${title}`,104,y+14,24,glyphs[ic],title===sideSelected?S.coral:S.blue);
      t(s,`二级导航文字 / ${title}`,title,147,y+13,144,16,title===sideSelected?S.coral:S.blue,title===sideSelected);
      if(title==='需求看板')menuTargets.push(it);
    });
    rect(s,'顶部工具栏 / 背景',316,0,1348,59,S.white);line(s,'顶部工具栏 / 下边线',316,58,1348);
    rect(s,'全局搜索 / 输入背景',340,0,618,43,S.gray,10);
    svg(s,'搜索图标',358,10,24,glyphs.search,S.blue);
    t(s,'搜索占位符','搜索项目、任务或文件...',392,10,465,17,S.muted);
    svg(s,'主题切换图标',1286,10,27,glyphs.sun,S.blue);
    svg(s,'消息通知图标',1351,9,28,glyphs.bell,S.blue);
    ellipse(s,'未读计数 / 红色圆点',1366,0,20,20,S.coral);
    t(s,'未读计数','4',1372,0,13,12,S.white,true);
    ellipse(s,'账户头像',1404,0,45,45,S.coral);
    t(s,'账户头像首字母','A',1418,5,25,25,S.white);
    t(s,'账户姓名','Ada (管理员)',1465,12,165,18,S.navy,true);
    svg(s,'账户下拉',1615,16,21,glyphs.chevron,S.blue);
    t(s,'页面标题',caption,360,76,430,31,S.navy,true);
    t(s,'页面副标题',subtitle,360,122,540,18,S.blue,true);
  }
  appChrome(home);
  appChrome(detail,'项目','项目管理','AragonTeam Platform','项目概览与研发协作');
  appChrome(board,'项目','需求看板','需求看板','AragonTeam Platform · 研发任务');
  const primaryBtn=button(home,'主操作 / 新建项目','新建项目',1476,78,166,49,S.coral,S.white,'plus');
  function card(s,name,badge,desc,initial,color,x,y,peopleMore){
    const c=rect(s,`项目卡片 / ${name}`,x,y,416,240,S.white,12,'#F3F4F8');
    rect(c,'项目头像 / 背景',20,18,65,65,color,11);
    t(c,'项目头像 / 字母',initial,41,22,35,36,initial==='A'?S.coral:'#148FE3');
    rect(c,'项目标识 / 胶囊底色',105,18,badge==='ARA'?54:55,29,S.label,15);
    t(c,'项目标识 / 文字',badge,118,25,39,14,S.coral,true);
    t(c,'项目名称',name,106,62,280,17,S.navy,true);
    svg(c,'外链图标',308,64,16,glyphs.external,'#315BCA');
    svg(c,'更多操作图标',376,17,19,glyphs.more,'#2756B3');
    t(c,'项目简介',desc,21,97,373,15,S.muted);
    line(c,'成员分隔线',20,130,375);
    ellipse(c,'管理员头像',21,144,31,31,S.coral);
    t(c,'管理员首字母','A',31,149,20,16,S.white,true);
    t(c,'管理员标识','Ada (管理员)',63,148,180,15,S.blue);
    const skin=['#F0BF9A','#ECB0A8','#E9C6A8','#D8A68F'];
    for(let i=0;i<4;i++){ellipse(c,`成员头像 ${i+1}`,265+i*23,146,27,27,skin[i]);t(c,`成员缩写 ${i+1}`,['李','王','张','陈'][i],272+i*23,150,14,11,S.navy,true)}
    t(c,'更多成员数量',`+${peopleMore}`,356,149,44,14,S.muted);
    const open=button(c,'快捷入口 / 打开项目','打开项目',20,184,190,42,S.pale,S.coral,'folder');
    const members=button(c,'快捷入口 / 成员','成员',221,184,175,42,S.gray,S.navy,'people');
    openTargets.push(open);memberTargets.push(members);
    return c;
  }
  card(home,'AragonTeam Platform','ARA','AI 时代的团队协作与研发管理平台自身。','A',S.label,355,163,13);
  card(home,'Legallens','123','Legallens','L',S.sky,787,163,14);
  // Details screen
  const back=button(detail,'返回项目列表','返回项目列表',360,164,165,44,S.pale,S.coral,'folder');
  const feature=rect(detail,'项目详情 / 顶部概览卡',360,232,900,194,S.white,12,S.border);
  rect(feature,'项目图标底色',25,25,67,67,S.label,10);t(feature,'项目图标文本','A',47,34,35,36,S.coral);
  t(feature,'项目标题','AragonTeam Platform',117,30,420,24,S.navy,true);
  t(feature,'项目介绍','AI 时代的团队协作与研发管理平台自身。',117,71,650,16,S.blue);
  line(feature,'详情分割线',25,118,850);
  t(feature,'负责人','负责人    Ada（管理员）',26,138,350,17,S.blue);
  t(feature,'研发成员','团队成员    17 人',440,138,250,17,S.blue);
  const goBoard=button(detail,'需求看板 / 打开入口','进入需求看板',360,453,200,48,S.coral,S.white,'board');
  const goPeople=button(detail,'成员管理 / 打开入口','查看项目成员',580,453,190,48,S.gray,S.navy,'people');
  const taskRows=[['待处理','8','待办事项'],['进行中','4','开发中任务'],['已完成','12','交付事项']];
  taskRows.forEach(([l,n,d],i)=>{const c=rect(detail,'项目指标 / '+l,360+i*310,536,292,120,S.white,12,S.border);t(c,'指标名称',l,20,16,250,17,S.blue);t(c,'指标数值',n,20,42,100,32,S.navy,true);t(c,'指标说明',d,20,90,170,13,S.muted)});
  // Kanban destination
  const kbBack=button(board,'看板 / 返回列表','返回项目',360,165,150,44,S.pale,S.coral,'folder');
  const columns=[['待处理',['梳理权限模型','整理项目文档']],['进行中',['项目首页交互','搜索体验优化']],['已完成',['设计系统建立','初始化项目仓库']]];
  columns.forEach(([label,cards],i)=>{const c=rect(board,'看板分组 / '+label,360+i*340,244,316,360,'#F3F6FB',12);t(c,'列标题',label,22,17,230,18,S.navy,true);t(c,'列数量',String(cards.length),267,18,30,15,S.muted);cards.forEach((v,j)=>{const task=rect(c,'任务卡片 / '+v,14,59+j*90,288,74,S.white,9);t(task,'任务标题',v,15,13,258,16,S.navy,true);t(task,'任务类型','研发任务 · AragonTeam Platform',15,44,258,12,S.muted)})});
  // overlay create project
  svg(createOverlay,'弹窗加号图标',26,27,33,glyphs.plus,S.coral);t(createOverlay,'弹窗标题','新建项目',70,28,340,25,S.navy,true);
  t(createOverlay,'输入项标记','项目名称 *',28,91,200,15,S.blue,true);
  rect(createOverlay,'项目名称 / 文本输入框',28,116,424,44,S.white,7,'#C9D8F0');t(createOverlay,'项目名称 / placeholder','例如：新产品研发',40,127,340,15,'#8497B7');
  t(createOverlay,'项目标识文字','项目标识',28,185,200,15,S.blue,true);
  rect(createOverlay,'项目标识 / 文本输入框',28,208,424,44,S.white,7,'#D9E2F0');t(createOverlay,'项目标识 / placeholder','例如：NEW',40,219,340,15,'#8497B7');
  t(createOverlay,'项目描述标签','项目描述',28,275,200,15,S.blue,true);
  rect(createOverlay,'项目描述 / 多行输入框',28,299,424,92,S.white,8,'#D9E2F0');t(createOverlay,'项目描述 / placeholder','简要介绍项目目标及范围',40,311,370,14,'#8497B7');
  const cancelCreate=button(createOverlay,'新建弹窗 / 取消','取消',250,421,88,42,S.gray,S.navy);
  const submitCreate=button(createOverlay,'新建弹窗 / 创建项目','创建项目',348,421,104,42,S.coral,S.white);
  // overlay members
  svg(memberOverlay,'成员弹窗图标',26,25,30,glyphs.people,S.coral);t(memberOverlay,'成员管理标题','项目成员',70,25,300,23,S.navy,true);
  [['Ada','管理员'],['李明','研发成员'],['王芳','设计师'],['张伟','开发工程师']].forEach(([n,r],i)=>{
    const y=88+i*63;
    ellipse(memberOverlay,'成员头像 / '+n,30,y,38,38,i===0?S.coral:i===1?'#8FB5ED':'#C5D6EF');
    t(memberOverlay,'成员姓名 / '+n,n,83,y+2,185,16,S.navy,true);
    t(memberOverlay,'成员角色 / '+n,r,292,y+5,145,14,S.muted);
    if(i<3)line(memberOverlay,'成员分隔线 '+i,82,y+55,340);
  });
  const closeMembers=button(memberOverlay,'成员弹窗 / 关闭','关闭',352,357,96,42,S.gray,S.navy);
  // Prototype connections
  await Promise.all([
    link(primaryBtn,createOverlay,'OVERLAY'),
    ...openTargets.map(n=>link(n,detail)),
    ...memberTargets.map(n=>link(n,memberOverlay,'OVERLAY')),
    link(back,home),link(goBoard,board),link(goPeople,memberOverlay,'OVERLAY'),link(kbBack,home),
    link(closeMembers,detail),link(cancelCreate,home),link(submitCreate,home),
  ]);
  // Connect secondary nav icons in home & detail, preserve intact editable nav structure
  for(const n of menuTargets){if(n.name.includes('需求看板'))await link(n,board);}
  // Bring user to design
  homePage.selection=[home];figma.viewport.scrollAndZoomIntoView([home]);
  figma.closePlugin(`已创建 ${created.length} 个可编辑图层、5 个交互画板、${linked} 条原型连接${linkErrors.length?`（${linkErrors.length} 条连接失败，需手动检查）`:""}。`);
})().catch(e=>{figma.closePlugin('生成失败：'+String(e&&e.message||e));});
