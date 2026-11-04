extends RefCounted
class_name AgentCatalog

const FACTIONS: Array[Dictionary] = [
	{
		"id": "value", "sprite_x": 0, "sprite_y": 0, "room_x": 0, "room_y": 0, "name": "价值派", "english": "VALUE & QUALITY", "analyst": "陈承远",
		"role": "资深价值投资经理", "room_name": "价值研究书房", "accent": "#e9c78d",
		
		"strategy": "寻找被低估的优质资产，以安全边际和长期现金流为核心。",
		"thesis": "在估值折价扩大、资产负债表稳健且现金流质量未恶化时分批建立仓位。",
		"bear": "盈利质量、资本开支或行业结构可能正在发生尚未反映在估值中的变化。",
		"risk": "限制单一标的集中度，若现金流与资产负债表同时恶化则撤销投资假设。",
		"signal": "自由现金流 · 估值折价 · 资本回报率", "quote": "价格是你付出的，价值才是你得到的。"
	},
	{
		"id": "growth", "sprite_x": 1, "sprite_y": 0, "room_x": 1, "room_y": 0, "name": "成长派", "english": "GROWTH", "analyst": "林亦菲",
		"role": "科技成长投资经理", "room_name": "成长创新实验室", "accent": "#65d8a5",
		
		"strategy": "寻找结构性增长曲线、技术迁移与可持续的收入加速。",
		"thesis": "当行业景气、收入动能和再投资回报同时改善时，提高成长资产配置。",
		"bear": "高增长预期可能已被估值充分计入，竞争加剧也可能压缩长期利润率。",
		"risk": "对高估值资产设置仓位上限，收入增速与现金消耗背离时降低风险敞口。",
		"signal": "收入加速度 · TAM 扩张 · 再投资回报", "quote": "投资未来，但必须为未来的价格负责。"
	},
	{
		"id": "trend", "sprite_x": 2, "sprite_y": 0, "room_x": 2, "room_y": 0, "name": "趋势派", "english": "TECHNICAL / MOMENTUM", "analyst": "陆子航",
		"role": "趋势交易经理", "room_name": "交易作战室", "accent": "#8db9ee",
		
		"strategy": "跟随价格动量与市场广度，在趋势确认后执行纪律化交易。",
		"thesis": "价格、相对强度和波动结构同向时顺势持有，趋势破坏时迅速降仓。",
		"bear": "动量信号可能滞后，跳空和震荡环境会造成连续假突破。",
		"risk": "以波动率调整仓位，设定趋势失效条件并控制换手成本。",
		"signal": "价格动量 · 相对强度 · 趋势广度", "quote": "不预测每一次波动，只执行已经确认的趋势。"
	},
	{
		"id": "quant", "sprite_x": 0, "sprite_y": 1, "room_x": 0, "room_y": 1, "name": "量化派", "english": "QUANT", "analyst": "周可秋",
		"role": "量化研究科学家", "room_name": "量化策略实验室", "accent": "#c6a1f2",
		
		"strategy": "通过统计信号、因子组合和风险预算寻找可重复的超额收益。",
		"thesis": "只有在信号稳定、样本外表现可接受且交易成本后仍有优势时才提高暴露。",
		"bear": "因子拥挤、数据偏差和市场结构变化可能令历史关系失效。",
		"risk": "限制因子集中与尾部风险，监测信号衰减、波动聚集和回撤。",
		"signal": "因子残差 · 信号稳定性 · 风险预算", "quote": "先证明统计优势，再让仓位表达观点。"
	},
	{
		"id": "sentiment", "sprite_x": 1, "sprite_y": 1, "room_x": 1, "room_y": 1, "name": "情绪派", "english": "SENTIMENT", "analyst": "苏念",
		"role": "市场心理分析师", "room_name": "舆情情报中心", "accent": "#f1a66e",
		
		"strategy": "观察注意力、预期差与拥挤交易，识别情绪反馈的拐点。",
		"thesis": "当情绪修复与价格确认共振时增加配置；过热且拥挤时主动收缩。",
		"bear": "情绪指标噪声大，叙事热度可能无法转化为基本面兑现。",
		"risk": "避免追逐单一热点，拥挤度上升和流动性下降时降低仓位。",
		"signal": "情绪温度 · 预期差 · 拥挤度", "quote": "市场不只是数字，也是不断变化的人心。"
	},
	{
		"id": "macro", "sprite_x": 2, "sprite_y": 1, "room_x": 2, "room_y": 1, "name": "宏观派", "english": "MACRO / REGIME", "analyst": "叶知秋",
		"role": "全球宏观策略师", "room_name": "全球策略会议室", "accent": "#7dd6df",
		
		"strategy": "从流动性、利率和经济周期识别风险偏好与资产定价状态。",
		"thesis": "在流动性与风险偏好同步改善时提高风险资产暴露，宏观压力上升时转向防御。",
		"bear": "宏观数据存在发布滞后与修订，政策预期可能快速反转。",
		"risk": "监测流动性冲击与相关性上升，避免单一宏观情景主导组合。",
		"signal": "流动性 · 利率路径 · 周期状态", "quote": "先判断风向，再决定帆该张多大。"
	}
]

static func all() -> Array[Dictionary]:
	return FACTIONS.duplicate(true)

static func ids() -> Array[String]:
	var result: Array[String] = []
	for faction in FACTIONS:
		result.append(str(faction.id))
	return result

static func get_faction(agent_id: String) -> Dictionary:
	for faction in FACTIONS:
		if str(faction.id) == agent_id:
			return faction.duplicate(true)
	return {}

static var _portrait_atlas: Texture2D
static var _room_atlas: Texture2D

static func portrait_texture(agent_id: String) -> Texture2D:
	var faction = get_faction(agent_id)
	if faction.is_empty():
		return null
	if _portrait_atlas == null:
		var image := Image.load_from_file("res://assets/agents-sprite.webp")
		if image == null or image.is_empty():
			return null
		_portrait_atlas = ImageTexture.create_from_image(image)
	if _portrait_atlas == null:
		return null
	var cell_size := Vector2(_portrait_atlas.get_width() / 3.0, _portrait_atlas.get_height() / 2.0)
	var texture := AtlasTexture.new()
	texture.atlas = _portrait_atlas
	texture.region = Rect2(Vector2(float(faction.sprite_x) * cell_size.x, float(faction.sprite_y) * cell_size.y), cell_size)
	return texture

static func room_texture(agent_id: String) -> Texture2D:
	var faction = get_faction(agent_id)
	if faction.is_empty():
		return null
	if _room_atlas == null:
		var image := Image.load_from_file("res://assets/rooms-sprite.webp")
		if image == null or image.is_empty():
			return null
		_room_atlas = ImageTexture.create_from_image(image)
	if _room_atlas == null:
		return null
	var cell_size := Vector2(_room_atlas.get_width() / 3.0, _room_atlas.get_height() / 2.0)
	var texture := AtlasTexture.new()
	texture.atlas = _room_atlas
	texture.region = Rect2(Vector2(float(faction.room_x) * cell_size.x, float(faction.room_y) * cell_size.y), cell_size)
	return texture

static func color_for(agent_id: String) -> Color:
	var faction = get_faction(agent_id)
	return Color(str(faction.get("accent", "#e9c78d")))
