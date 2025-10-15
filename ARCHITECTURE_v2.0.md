# PyMD Editor v2.0 - 企业级智能编辑器架构设计

## 📋 项目概述

PyMD Editor v2.0 将从简单的Markdown编辑器升级为RAG增强的多行业智能编辑器，支持AI辅助创作、知识库管理和行业定制化。

### 核心愿景
- **智能化**：AI驱动的内容创作和优化
- **知识化**：企业知识库的沉淀和复用
- **专业化**：垂直行业深度定制
- **开放化**：插件化架构，易于扩展

## 🏗️ 整体架构

```
PyMD Editor v2.0 架构图
┌─────────────────────────────────────────────────────────────┐
│                   PyMD Editor Core                          │
├──────────────┬──────────────────┬──────────────────────────┤
│  Editor      │    Preview/      │    AI Assistant +        │
│  Pane        │    WYSIWYG       │    Knowledge Base        │
│              │                  │                          │
│  40%         │    40%           │    20% (expandable)      │
└──────────────┴──────────────────┴──────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                Knowledge Engine                             │
├─────────────────┬─────────────────┬─────────────────────────┤
│  Document       │   AI Providers  │   Industry Adapters     │
│  Processors     │                 │                         │
│                 │                 │                         │
│  • PDF Reader   │  • Personal AI  │  • Advertising Module  │
│  • Word Parser  │  • Gemini API   │  • Accounting Module   │
│  • Excel Reader │  • Smart Router │  • Legal Module        │
│  • Folder Scan  │                 │  • Medical Module      │
└─────────────────┴─────────────────┴─────────────────────────┘
```

## 🎯 核心功能模块

### 1. 三栏布局系统

#### 布局配置
```python
class ThreeColumnLayout:
    """响应式三栏布局管理器"""
    
    # 布局模式
    layouts = {
        "default":       [40%, 40%, 20%],  # 默认均衡布局
        "focus_writing": [60%, 40%,  0%],  # 专注写作模式
        "ai_intensive":  [30%, 30%, 40%],  # AI辅助模式  
        "preview_only":  [40%, 60%,  0%],  # 预览优先模式
    }
    
    def adjust_layout(self, mode: str):
        """动态调整布局比例"""
        pass
        
    def save_user_preference(self, layout: List[float]):
        """保存用户自定义布局"""
        pass
```

#### 用户体验设计
- **可拖拽分割线**：实时调整面板大小
- **一键布局切换**：工具栏快速切换预设
- **智能响应式**：根据窗口大小自动调整
- **状态记忆**：保存用户偏好设置

### 2. AI集成与智能路由

#### AI服务提供商架构
```python
class AIProvider(ABC):
    """AI服务提供商抽象基类"""
    
    @abstractmethod
    async def generate(self, prompt: str, context: dict) -> AIResponse:
        """生成AI响应"""
        pass
    
    @abstractmethod
    def get_cost_estimate(self, prompt: str) -> float:
        """估算调用成本"""
        pass
    
    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """获取AI能力列表"""
        pass

class PersonalAIProvider(AIProvider):
    """个人免费AI服务 - https://dataflowxx.dpdns.org"""
    
    base_url = "https://dataflowxx.dpdns.org"
    cost = 0.0  # 完全免费
    
    capabilities = [
        "text_generation",
        "text_improvement", 
        "brainstorming",
        "grammar_check",
        "simple_qa"
    ]
    
class GeminiProvider(AIProvider):
    """Google Gemini API服务"""
    
    base_url = "https://generativelanguage.googleapis.com"
    cost_per_1k = 0.002  # 每1K tokens成本
    
    capabilities = [
        "advanced_reasoning",
        "code_generation",
        "long_text_analysis", 
        "multi_language",
        "complex_qa",
        "document_analysis"
    ]
```

#### 智能路由逻辑
```python
class AIRouter:
    """智能AI调用路由器"""
    
    def route_request(self, task_type: str, content: str, user_pref: dict) -> AIProvider:
        """
        智能选择最适合的AI服务
        
        路由策略：
        1. 任务复杂度分析
        2. 用户预算偏好
        3. 服务可用性检查
        4. 负载均衡考虑
        """
        
        # 简单任务优先使用免费AI
        if self._is_simple_task(task_type, content):
            return PersonalAIProvider()
            
        # 复杂任务需要高级AI
        elif self._requires_advanced_ai(task_type, content):
            return GeminiProvider()
            
        # 负载均衡和容错
        else:
            return self._select_best_available([
                PersonalAIProvider(),
                GeminiProvider()
            ])
    
    def _is_simple_task(self, task_type: str, content: str) -> bool:
        """判断是否为简单任务"""
        simple_tasks = [
            "grammar_check",
            "text_polish", 
            "brainstorming",
            "simple_qa"
        ]
        
        return (task_type in simple_tasks or 
                len(content) < 500 or
                not self._contains_complex_requirements(content))
```

### 3. 知识库与文档处理系统

#### 文档处理器架构
```python
class DocumentProcessor(ABC):
    """文档处理器抽象基类"""
    
    @abstractmethod
    def extract_text(self, file_path: str) -> str:
        """提取纯文本内容"""
        pass
    
    @abstractmethod 
    def extract_structure(self, file_path: str) -> DocumentStructure:
        """提取文档结构信息"""
        pass
    
    @abstractmethod
    def get_metadata(self, file_path: str) -> dict:
        """获取文档元数据"""
        pass

class PDFProcessor(DocumentProcessor):
    """PDF文档处理器"""
    
    def extract_text(self, file_path: str) -> str:
        """使用PyPDF2或pdfplumber提取文本"""
        pass
    
    def extract_structure(self, file_path: str) -> DocumentStructure:
        """提取章节、表格、图片等结构信息"""
        pass

class WordProcessor(DocumentProcessor):
    """Word文档处理器"""
    
    def extract_text(self, file_path: str) -> str:
        """使用python-docx提取内容"""
        pass
        
class ExcelProcessor(DocumentProcessor):
    """Excel文档处理器"""
    
    def extract_text(self, file_path: str) -> str:
        """使用pandas读取表格数据"""
        pass

class FolderProcessor:
    """文件夹批量处理器"""
    
    def scan_folder(self, folder_path: str, recursive: bool = True) -> List[DocumentInfo]:
        """扫描文件夹，返回所有可处理文件信息"""
        pass
```

#### 混合检索系统
```python
class KnowledgeBase:
    """企业知识库管理系统"""
    
    def __init__(self):
        self.vector_db = ChromaDB()      # 向量数据库 - 语义检索
        self.text_index = WhooshIndex()  # 全文索引 - 精确匹配
        self.metadata_db = SQLiteDB()    # 元数据存储
    
    def add_document(self, doc_path: str, industry: str = None):
        """添加文档到知识库"""
        
        # 1. 文档处理
        processor = self._get_processor(doc_path)
        content = processor.extract_text(doc_path)
        structure = processor.extract_structure(doc_path)
        metadata = processor.get_metadata(doc_path)
        
        # 2. 文本分块
        chunks = self._chunk_text(content, chunk_size=512, overlap=50)
        
        # 3. 向量嵌入
        embeddings = self._generate_embeddings(chunks)
        
        # 4. 索引存储
        self.vector_db.add(chunks, embeddings, metadata)
        self.text_index.add_document(content, metadata)
        self.metadata_db.insert(doc_path, metadata, industry)
    
    def search(self, query: str, method: str = "hybrid", top_k: int = 5) -> List[SearchResult]:
        """混合检索方法"""
        
        if method == "vector":
            # 纯语义检索 - 适合概念性查询
            return self.vector_db.similarity_search(query, k=top_k)
            
        elif method == "keyword":  
            # 纯关键词检索 - 适合精确匹配
            return self.text_index.search(query, limit=top_k)
            
        elif method == "hybrid":
            # 混合检索 - 平衡语义和精确性
            vector_results = self.vector_db.similarity_search(query, k=top_k)
            keyword_results = self.text_index.search(query, limit=top_k)
            
            # RRF (Reciprocal Rank Fusion) 结果融合
            return self._merge_results(vector_results, keyword_results)
```

### 4. 多行业适配系统

#### 插件化行业模块
```python
class IndustryAdapter(ABC):
    """行业适配器抽象基类"""
    
    @abstractmethod
    def get_name(self) -> str:
        """获取行业名称"""
        pass
    
    @abstractmethod
    def get_templates(self) -> List[Template]:
        """获取行业文档模板"""
        pass
    
    @abstractmethod
    def get_terminology(self) -> Dict[str, str]:
        """获取行业专业术语库"""
        pass
    
    @abstractmethod
    def get_ai_prompts(self) -> Dict[str, str]:
        """获取行业专用AI提示词"""
        pass
    
    @abstractmethod
    def get_compliance_rules(self) -> List[ComplianceRule]:
        """获取行业合规检查规则"""
        pass

# 广告行业适配器
class AdvertisingAdapter(IndustryAdapter):
    """广告营销行业适配器"""
    
    name = "advertising"
    
    templates = [
        "social_media_post.md",      # 社交媒体文案
        "product_description.md",    # 产品描述
        "campaign_brief.md",         # 营销活动简报
        "brand_story.md",            # 品牌故事
        "press_release.md"           # 新闻稿
    ]
    
    terminology = {
        "CTR": "Click-Through Rate (点击转化率)",
        "ROI": "Return on Investment (投资回报率)", 
        "KOL": "Key Opinion Leader (关键意见领袖)",
        "CPC": "Cost Per Click (每次点击成本)",
        "CPM": "Cost Per Mille (千次展示成本)",
        "ROAS": "Return on Ad Spend (广告支出回报率)"
    }
    
    ai_prompts = {
        "creative_brainstorm": "作为资深广告创意，请为{product}生成5个创意方向...",
        "copy_optimization": "请优化这段广告文案，提升转化率...", 
        "audience_analysis": "分析目标受众特征，制定传播策略...",
        "competitor_analysis": "分析竞品营销策略，找出差异化机会..."
    }

# 会计行业适配器  
class AccountingAdapter(IndustryAdapter):
    """会计财务行业适配器"""
    
    name = "accounting"
    
    templates = [
        "financial_report.md",       # 财务报告
        "audit_checklist.md",        # 审计检查清单
        "tax_summary.md",            # 税务汇总
        "budget_analysis.md",        # 预算分析
        "compliance_memo.md"         # 合规备忘录
    ]
    
    terminology = {
        "GAAP": "Generally Accepted Accounting Principles (公认会计准则)",
        "EBITDA": "Earnings Before Interest, Tax, Depreciation, Amortization (息税折旧摊销前利润)",
        "NPV": "Net Present Value (净现值)",
        "IRR": "Internal Rate of Return (内部收益率)",
        "WACC": "Weighted Average Cost of Capital (加权平均资本成本)"
    }
    
    ai_prompts = {
        "financial_analysis": "请分析这份财务数据，识别关键趋势和风险...",
        "compliance_check": "检查文档是否符合{standard}会计准则...",
        "ratio_analysis": "计算并解释这些财务比率的含义...",
        "forecast_review": "评估财务预测的合理性和风险..."
    }
```

#### 配置驱动的行业定制
```python
class IndustryManager:
    """行业管理器"""
    
    def __init__(self):
        self.adapters = {}
        self.current_industry = None
        
    def register_adapter(self, adapter: IndustryAdapter):
        """注册行业适配器"""
        self.adapters[adapter.get_name()] = adapter
        
    def switch_industry(self, industry_name: str):
        """切换当前行业"""
        if industry_name in self.adapters:
            self.current_industry = industry_name
            self._load_industry_resources()
    
    def _load_industry_resources(self):
        """加载行业资源"""
        adapter = self.adapters[self.current_industry]
        
        # 加载模板
        self._load_templates(adapter.get_templates())
        
        # 加载术语库
        self._load_terminology(adapter.get_terminology())
        
        # 配置AI提示词
        self._configure_ai_prompts(adapter.get_ai_prompts())

# 配置文件结构
class IndustryConfig:
    """
    行业配置文件结构
    
    config/industries/
    ├── advertising/
    │   ├── templates/
    │   ├── terminology.json
    │   ├── ai_prompts.yaml
    │   └── compliance_rules.json
    └── accounting/
        ├── templates/
        ├── terminology.json 
        ├── ai_prompts.yaml
        └── compliance_rules.json
    """
    
    def load_config(self, industry: str) -> dict:
        """从配置文件加载行业设置"""
        config_path = f"config/industries/{industry}/"
        
        return {
            "templates": self._load_templates(config_path + "templates/"),
            "terminology": self._load_json(config_path + "terminology.json"),
            "ai_prompts": self._load_yaml(config_path + "ai_prompts.yaml"),
            "compliance": self._load_json(config_path + "compliance_rules.json")
        }
```

## 🎯 系统优势分析

### 技术优势

1. **模块化架构**
   - 松耦合设计，各模块独立开发和测试
   - 插件化行业适配，易于扩展新领域
   - 统一接口设计，降低维护成本

2. **智能化程度高**
   - AI智能路由，自动选择最优服务
   - 混合检索技术，提升搜索准确度
   - 上下文感知，提供精准建议

3. **性能与扩展性**
   - 异步处理，提升响应速度
   - 分层缓存，减少重复计算
   - 水平扩展，支持企业级部署

### 商业优势

1. **成本控制**
   - 免费AI优先策略，降低使用成本
   - 智能升级机制，按需使用付费服务
   - 本地知识库，减少外部API依赖

2. **差异化竞争**
   - 垂直行业深度定制
   - 企业知识沉淀和复用
   - 一站式工作流解决方案

3. **商业模式灵活**
   - 免费基础版 + 付费行业版
   - SaaS订阅 + 私有部署
   - API代理 + 咨询服务

### 用户体验优势

1. **学习曲线平滑**
   - 渐进式功能披露
   - 智能提示和引导
   - 个性化界面配置

2. **工作效率提升**
   - AI辅助内容创作
   - 知识库快速检索
   - 模板和术语自动补全

3. **专业性强**
   - 行业术语准确性
   - 合规性自动检查
   - 专业模板和流程

## 🚀 实施路线图

### Phase 1: 基础架构 (2-3周)
```
Week 1: 三栏布局重构
- 实现可拖拽分割线
- 添加布局预设功能
- 优化响应式设计

Week 2-3: AI集成框架
- 接入Personal AI服务
- 实现Gemini API调用
- 构建智能路由逻辑
```

### Phase 2: 知识库系统 (3-4周)
```
Week 1: 文档处理器
- PDF/Word/Excel处理
- 文件夹批量扫描
- 文本分块和清洗

Week 2-3: 检索系统
- 向量数据库集成
- 全文索引构建
- 混合检索算法

Week 4: 知识管理界面
- 文档导入界面
- 搜索结果展示
- 知识库管理功能
```

### Phase 3: 行业适配 (2-3周)
```
Week 1: 插件架构
- 行业适配器框架
- 配置文件系统
- 动态加载机制

Week 2: 示例行业模块
- 广告营销适配器
- 会计财务适配器
- 模板和术语库

Week 3: 行业切换界面
- 行业选择器
- 资源热加载
- 用户偏好保存
```

### Phase 4: 优化与完善 (2周)
```
Week 1: 性能优化
- 异步处理优化
- 缓存策略完善
- 内存使用优化

Week 2: 用户体验
- 界面细节优化
- 快捷键支持
- 帮助文档完善
```

## 📊 技术栈选型

### 核心框架
- **GUI**: PyQt6 (成熟稳定的桌面应用框架)
- **AI集成**: httpx + asyncio (异步HTTP客户端)
- **向量数据库**: ChromaDB (轻量级向量存储)
- **全文检索**: Whoosh (纯Python搜索引擎)
- **文档处理**: PyPDF2, python-docx, pandas

### 依赖库更新
```txt
# 新增依赖
chromadb>=0.4.0          # 向量数据库
whoosh>=2.7.4            # 全文搜索
httpx>=0.25.0            # 异步HTTP客户端
sentence-transformers>=2.2.2  # 文本嵌入
PyPDF2>=3.0.0            # PDF处理
openpyxl>=3.1.0          # Excel处理
pyyaml>=6.0              # 配置文件解析
```

## 🔧 关键设计决策

### 1. AI服务优先级策略
- **免费优先**: 优先使用Personal AI，降低成本
- **智能升级**: 复杂任务自动切换到Gemini API
- **用户控制**: 允许用户强制指定AI服务
- **容错机制**: 服务不可用时自动降级

### 2. 知识库存储策略
- **本地优先**: 保护企业数据隐私
- **混合存储**: 向量+全文+元数据分离存储
- **增量更新**: 支持文档修改后的增量同步
- **版本管理**: 跟踪文档版本和变更历史

### 3. 行业适配策略
- **配置驱动**: 避免硬编码，提高灵活性
- **插件化**: 支持第三方行业插件
- **渐进加载**: 按需加载行业资源
- **向下兼容**: 新行业不影响现有功能

### 4. 用户界面策略
- **渐进披露**: 新用户看到简化界面
- **专业模式**: 高级用户可启用全部功能
- **自适应**: 根据使用习惯调整界面
- **可访问性**: 支持键盘操作和屏幕阅读器

## 🎯 成功指标

### 技术指标
- **响应速度**: AI调用 < 3秒，搜索 < 1秒
- **准确率**: 知识库搜索相关度 > 85%
- **稳定性**: 系统可用性 > 99%
- **扩展性**: 支持 10万+ 文档索引

### 用户指标  
- **学习成本**: 新用户 30分钟上手
- **效率提升**: 文档创作效率提升 50%+
- **用户满意度**: NPS > 50
- **功能使用率**: AI辅助功能使用率 > 60%

### 商业指标
- **用户转化**: 免费用户到付费用户转化率 > 15%
- **用户留存**: 月活跃用户留存率 > 70%
- **收入增长**: 月收入环比增长 > 20%
- **市场占有率**: 目标行业市场份额 > 5%

---

**架构设计版本**: v2.0.0-draft  
**设计时间**: 2025年10月15日  
**下次更新**: 根据实施进展调整细节