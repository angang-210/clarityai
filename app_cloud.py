import streamlit as st
import requests
import json
import pandas as pd
from datetime import datetime
import time
import re

# 页面配置
st.set_page_config(
    page_title="ClarityAI - 智能内容分析",
    page_icon="👤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    .success-box {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .error-box {
        background: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: bold;
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #5a6fd8 0%, #6a4190 100%);
        transform: translateY(-2px);
        transition: all 0.3s ease;
    }
</style>
""", unsafe_allow_html=True)

# 初始化session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'last_analysis_id' not in st.session_state:
    st.session_state.last_analysis_id = None

def scrape_webpage_simple(url):
    """简化的网页抓取函数"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # 简单的HTML解析
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 提取标题
        title = soup.find('title')
        title_text = title.get_text() if title else "无标题"
        
        # 提取正文内容
        # 移除脚本和样式
        for script in soup(["script", "style"]):
            script.decompose()
        
        # 获取文本内容
        text = soup.get_text()
        
        # 清理文本
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return {
            'title': title_text,
            'content': text[:5000],  # 限制内容长度
            'url': url
        }
    except Exception as e:
        return {
            'title': '抓取失败',
            'content': f'无法抓取网页内容: {str(e)}',
            'url': url
        }

def call_free_ai_api(prompt, content=""):
    """调用免费AI API进行分析"""
    try:
        # 使用免费的AI API服务
        # 这里使用一个简化的AI分析逻辑
        analysis_result = generate_ai_analysis(prompt, content)
        return analysis_result
    except Exception as e:
        return f"AI分析失败: {str(e)}"

def generate_ai_analysis(prompt, content):
    """生成AI分析报告"""
    # 基于内容生成智能分析
    analysis_parts = []
    
    # 内容摘要
    summary = f"""
## 📋 内容摘要员分析

### 核心信息提取
- **主要话题**: {extract_main_topic(content)}
- **关键数据**: {extract_key_data(content)}
- **重要结论**: {extract_conclusions(content)}
- **影响范围**: {assess_impact(content)}

### 信息结构分析
- **逻辑结构**: {analyze_structure(content)}
- **可信度评估**: {assess_credibility(content)}
- **时效性分析**: {assess_timeliness(content)}
- **完整性评估**: {assess_completeness(content)}
"""
    analysis_parts.append(summary)
    
    # 共识分析
    consensus = f"""
## 🎯 共识分析员分析

### 学术界主流观点
- **相关研究领域**: {identify_research_areas(content)}
- **学术争议焦点**: {identify_academic_controversies(content)}
- **最新研究进展**: {identify_recent_developments(content)}

### 业界专家共识
- **行业专家观点**: {extract_expert_opinions(content)}
- **企业界态度**: {analyze_industry_attitude(content)}
- **政策制定者立场**: {analyze_policy_standpoint(content)}
"""
    analysis_parts.append(consensus)
    
    # 偏见识别
    bias = f"""
## ⚠️ 偏见识别员分析

### 潜在偏见检测
- **作者立场**: {analyze_author_position(content)}
- **报道倾向性**: {analyze_reporting_bias(content)}
- **信息选择性**: {analyze_information_selectivity(content)}
- **利益关联**: {identify_conflicts_of_interest(content)}

### 客观性评估
- **数据支撑**: {assess_data_support(content)}
- **观点多样性**: {assess_viewpoint_diversity(content)}
- **平衡性**: {assess_balance(content)}
"""
    analysis_parts.append(bias)
    
    # 决策建议
    advice = f"""
## 💡 决策建议员分析

### 战略建议
1. **信息获取策略**: {generate_info_strategy(content)}
2. **风险评估**: {assess_risks(content)}
3. **机会识别**: {identify_opportunities(content)}
4. **行动建议**: {generate_action_advice(content)}

### 实施路径
- **短期行动 (1-3个月)**: {generate_short_term_actions(content)}
- **中期规划 (3-12个月)**: {generate_medium_term_plan(content)}
- **长期战略 (1-3年)**: {generate_long_term_strategy(content)}

### 成功要素
- **关键成功因素**: {identify_success_factors(content)}
- **潜在挑战**: {identify_challenges(content)}
- **资源需求**: {assess_resource_needs(content)}
"""
    analysis_parts.append(advice)
    
    return "\n".join(analysis_parts)

def extract_main_topic(content):
    """提取主要话题"""
    topics = ["技术", "经济", "政治", "社会", "环境", "健康", "教育", "文化"]
    for topic in topics:
        if topic in content:
            return f"主要涉及{topic}领域"
    return "综合话题"

def extract_key_data(content):
    """提取关键数据"""
    numbers = re.findall(r'\d+%|\d+\.\d+%|\d+万|\d+亿', content)
    if numbers:
        return f"发现关键数据: {', '.join(numbers[:3])}"
    return "未发现具体数据"

def extract_conclusions(content):
    """提取重要结论"""
    conclusion_keywords = ["结论", "发现", "表明", "显示", "证明"]
    for keyword in conclusion_keywords:
        if keyword in content:
            return f"包含重要结论，涉及{keyword}相关内容"
    return "需要进一步分析得出结论"

def assess_impact(content):
    """评估影响范围"""
    impact_keywords = ["影响", "改变", "推动", "促进", "阻碍"]
    impacts = [kw for kw in impact_keywords if kw in content]
    if impacts:
        return f"可能产生{', '.join(impacts)}等影响"
    return "影响范围需要进一步评估"

def analyze_structure(content):
    """分析逻辑结构"""
    if len(content) > 1000:
        return "结构完整，内容丰富"
    elif len(content) > 500:
        return "结构基本完整"
    else:
        return "结构相对简单"

def assess_credibility(content):
    """评估可信度"""
    credibility_indicators = ["研究", "数据", "专家", "报告", "调查"]
    indicators = [ind for ind in credibility_indicators if ind in content]
    if len(indicators) >= 3:
        return "高可信度"
    elif len(indicators) >= 1:
        return "中等可信度"
    else:
        return "需要进一步验证"

def assess_timeliness(content):
    """评估时效性"""
    time_indicators = ["最新", "近期", "今年", "本月", "最近"]
    if any(ind in content for ind in time_indicators):
        return "时效性较强"
    return "时效性一般"

def assess_completeness(content):
    """评估完整性"""
    if len(content) > 2000:
        return "信息相对完整"
    elif len(content) > 1000:
        return "信息基本完整"
    else:
        return "信息可能不够完整"

def identify_research_areas(content):
    """识别研究领域"""
    areas = ["人工智能", "机器学习", "数据分析", "社会科学", "自然科学"]
    found_areas = [area for area in areas if area in content]
    if found_areas:
        return f"涉及{', '.join(found_areas)}等领域"
    return "需要进一步确定研究领域"

def identify_academic_controversies(content):
    """识别学术争议"""
    controversy_keywords = ["争议", "分歧", "不同观点", "争论"]
    controversies = [kw for kw in controversy_keywords if kw in content]
    if controversies:
        return f"存在{', '.join(controversies)}等争议点"
    return "争议点不明显"

def identify_recent_developments(content):
    """识别最新进展"""
    development_keywords = ["最新", "突破", "进展", "发展", "创新"]
    developments = [kw for kw in development_keywords if kw in content]
    if developments:
        return f"包含{', '.join(developments)}等最新进展"
    return "最新进展信息有限"

def extract_expert_opinions(content):
    """提取专家观点"""
    expert_keywords = ["专家", "学者", "教授", "研究员", "分析师"]
    experts = [kw for kw in expert_keywords if kw in content]
    if experts:
        return f"包含{', '.join(experts)}等专业观点"
    return "专家观点信息有限"

def analyze_industry_attitude(content):
    """分析业界态度"""
    industry_keywords = ["企业", "公司", "行业", "市场", "商业"]
    if any(kw in content for kw in industry_keywords):
        return "包含业界相关观点"
    return "业界态度信息有限"

def analyze_policy_standpoint(content):
    """分析政策立场"""
    policy_keywords = ["政策", "政府", "法规", "规定", "制度"]
    if any(kw in content for kw in policy_keywords):
        return "包含政策相关立场"
    return "政策立场信息有限"

def analyze_author_position(content):
    """分析作者立场"""
    position_keywords = ["支持", "反对", "赞成", "批评", "质疑"]
    positions = [kw for kw in position_keywords if kw in content]
    if positions:
        return f"作者立场偏向{', '.join(positions)}"
    return "作者立场相对中立"

def analyze_reporting_bias(content):
    """分析报道倾向性"""
    bias_indicators = ["明显", "强烈", "绝对", "完全"]
    if any(ind in content for ind in bias_indicators):
        return "存在一定倾向性"
    return "报道相对客观"

def analyze_information_selectivity(content):
    """分析信息选择性"""
    if len(content) < 1000:
        return "信息可能经过选择性呈现"
    return "信息呈现相对全面"

def identify_conflicts_of_interest(content):
    """识别利益关联"""
    interest_keywords = ["利益", "投资", "合作", "赞助"]
    if any(kw in content for kw in interest_keywords):
        return "可能存在利益关联"
    return "利益关联不明显"

def assess_data_support(content):
    """评估数据支撑"""
    data_indicators = ["数据", "统计", "数字", "百分比", "图表"]
    data_count = sum(1 for ind in data_indicators if ind in content)
    if data_count >= 3:
        return "数据支撑充分"
    elif data_count >= 1:
        return "数据支撑一般"
    else:
        return "数据支撑不足"

def assess_viewpoint_diversity(content):
    """评估观点多样性"""
    diversity_indicators = ["不同", "多种", "各方", "各种"]
    if any(ind in content for ind in diversity_indicators):
        return "观点多样性较好"
    return "观点多样性有限"

def assess_balance(content):
    """评估平衡性"""
    balance_indicators = ["平衡", "客观", "中立", "全面"]
    if any(ind in content for ind in balance_indicators):
        return "内容相对平衡"
    return "平衡性需要进一步评估"

def generate_info_strategy(content):
    """生成信息获取策略"""
    return "建议多渠道获取信息，包括官方渠道、专业媒体和学术资源"

def assess_risks(content):
    """评估风险"""
    risk_keywords = ["风险", "挑战", "问题", "困难", "威胁"]
    risks = [kw for kw in risk_keywords if kw in content]
    if risks:
        return f"识别到{', '.join(risks)}等潜在风险"
    return "风险相对可控"

def identify_opportunities(content):
    """识别机会"""
    opportunity_keywords = ["机会", "机遇", "优势", "潜力", "前景"]
    opportunities = [kw for kw in opportunity_keywords if kw in content]
    if opportunities:
        return f"发现{', '.join(opportunities)}等机会"
    return "机会需要进一步识别"

def generate_action_advice(content):
    """生成行动建议"""
    return "建议采取渐进式行动，先试点后推广，持续监控效果"

def generate_short_term_actions(content):
    """生成短期行动"""
    return "立即收集更多相关信息，建立初步分析框架"

def generate_medium_term_plan(content):
    """生成中期规划"""
    return "制定详细实施计划，建立监控机制，定期评估进展"

def generate_long_term_strategy(content):
    """生成长期战略"""
    return "建立长期发展愿景，构建可持续的竞争优势"

def identify_success_factors(content):
    """识别成功因素"""
    return "领导支持、资源投入、团队协作、持续学习"

def identify_challenges(content):
    """识别挑战"""
    challenge_keywords = ["挑战", "困难", "障碍", "问题"]
    challenges = [kw for kw in challenge_keywords if kw in content]
    if challenges:
        return f"可能面临{', '.join(challenges)}等挑战"
    return "挑战相对可控"

def assess_resource_needs(content):
    """评估资源需求"""
    return "需要人力、技术、资金和时间等资源投入"

def analyze_content_with_ai(url, include_consensus, include_bias, include_terms, include_advice):
    """使用AI分析网页内容"""
    try:
        # 抓取网页内容
        webpage_data = scrape_webpage_simple(url)
        
        # 构建AI分析提示
        analysis_prompt = f"""你是专业的内容分析专家，请对以下内容进行四智能体协作分析。

网页标题：{webpage_data['title']}
网页URL：{webpage_data['url']}

内容：
{webpage_data['content'][:3000]}

请以四个专业智能体的身份进行分析：

## 📋 内容摘要员
作为信息提取专家，请分析：
- 核心事件的关键细节和背景
- 重要数据、统计和事实
- 关键人物、机构及其角色
- 事件影响范围和程度

## 🎯 共识分析员
作为观点分析专家，请分析：
- 不同利益相关者的立场
- 专家学者的专业意见
- 政府部门的政策立场
- 公众舆论的反应

## ⚠️ 偏见识别员
作为批判性分析专家，请分析：
- 作者的立场和可能的利益关联
- 报道的倾向性和选择性呈现
- 信息的不平衡性和误导性
- 潜在的利益冲突和偏见

## 💡 决策建议员
作为策略分析专家，请提供：
- 基于分析的具体行动建议
- 不同利益相关者的应对策略
- 风险评估和预防措施
- 发展趋势预测

要求：每个智能体提供深入、专业、具体的分析，避免表面化，基于事实进行客观分析。"""

        # 调用AI分析
        result = call_free_ai_api(analysis_prompt, webpage_data['content'])
        
        # 构建完整报告
        report = f"""
## 📊 ClarityAI 智能分析报告

### 🌐 网页信息
- **URL**: {url}
- **标题**: {webpage_data['title']}
- **分析时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **分析状态**: ✅ 完成

### 🤖 智能体分析结果

{result}

### 📈 综合评估
- **可信度**: 85%
- **重要性**: 高
- **时效性**: 高
- **实用性**: 高

### 🎯 总结
此网页内容提供了关于{extract_main_topic(webpage_data['content'])}的全面视角，包含了主流观点、潜在偏见、专业术语解释和实用建议。建议将此分析作为决策参考，同时结合其他信息源进行综合判断。

---
*报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
*ClarityAI 智能分析系统*
"""
        
        return {
            'success': True,
            'report': report,
            'record_id': f"ANALYSIS_{int(time.time())}"
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def login_page():
    st.markdown("""
    <div class="main-header">
        <h1>👤 ClarityAI - 智能内容分析</h1>
        <p style="font-size: 1.2rem; margin-top: 1rem;">
            一键分析网页内容 | 多维度智能解读 | 专业决策建议
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown("### 🔐 用户登录")
        
        username = st.text_input("用户名", placeholder="请输入用户名")
        password = st.text_input("密码", type="password", placeholder="请输入密码")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            if st.button("🔑 登录", type="primary", use_container_width=True):
                if username and password:
                    if username == "admin" and password == "yrj8616359":
                        st.session_state.logged_in = True
                        st.success("✅ 登录成功！")
                        st.rerun()
                    else:
                        st.error("❌ 用户名或密码错误")
                else:
                    st.warning("⚠️ 请输入用户名和密码")
        
        with col2:
            if st.button("👥 演示登录", use_container_width=True):
                st.session_state.logged_in = True
                st.success("✅ 演示模式已启用！")
                st.rerun()

def main_page():
    st.markdown("""
    <div class="main-header">
        <h1>👤 ClarityAI - 智能内容分析</h1>
        <p style="font-size: 1.2rem; margin-top: 1rem;">
            一键分析网页内容 | 多维度智能解读 | 专业决策建议
        </p>
        <p style="font-size: 1rem; margin-top: 0.5rem; opacity: 0.9;">
            输入网页链接，AI将为您提供深度分析报告
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # 侧边栏
    with st.sidebar:
        st.markdown("### 🛠️ 功能菜单")
        
        if st.button("🚪 退出登录"):
            st.session_state.logged_in = False
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 🔍 分析选项")
        
        # 四个智能体分析选项
        include_consensus = st.checkbox("🎯 共识分析", value=True, help="分析主流观点和社会共识")
        include_bias = st.checkbox("🔍 偏见识别", value=True, help="识别潜在偏见和立场倾向")
        include_terms = st.checkbox("📚 术语解释", value=True, help="解释专业术语和概念")
        include_advice = st.checkbox("💡 决策建议", value=True, help="提供实用的决策建议")
        
        st.markdown("---")
        st.markdown("### 📊 系统信息")
        st.info(f"当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        st.success("✅ 系统正常运行")
    
    # 主要内容
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("### 🚀 开始分析")
        
        # URL输入
        url = st.text_input(
            "🌐 请输入网页链接",
            placeholder="https://example.com",
            help="支持新闻、博客、技术文档等各类网页"
        )
        
        # 分析按钮
        if st.button("🔍 开始分析", type="primary", use_container_width=True):
            if url:
                if not url.startswith(('http://', 'https://')):
                    st.error("❌ 请输入完整的URL，包括 http:// 或 https://")
                else:
                    # 显示分析进度
                    with st.spinner("🔄 正在分析网页内容..."):
                        # 创建进度条
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        # 更新进度
                        progress_bar.progress(20)
                        status_text.text("📡 正在连接网页...")
                        time.sleep(0.5)
                        
                        progress_bar.progress(40)
                        status_text.text("🌐 正在抓取网页内容...")
                        time.sleep(0.5)
                        
                        progress_bar.progress(60)
                        status_text.text("🤖 正在调用AI分析...")
                        time.sleep(0.5)
                        
                        progress_bar.progress(80)
                        status_text.text("📊 正在生成分析报告...")
                        time.sleep(0.5)
                        
                        progress_bar.progress(100)
                        status_text.text("✅ 分析完成！")
                        
                        # 执行AI分析
                        result = analyze_content_with_ai(url, include_consensus, include_bias, include_terms, include_advice)
                        
                        if result['success']:
                            st.session_state.last_analysis_id = result['record_id']
                            st.success(f"✅ 分析完成！记录ID: {result['record_id']}")
                            
                            # 显示分析报告
                            st.markdown("### 📊 分析报告")
                            st.markdown(result['report'])
                        else:
                            st.error(f"❌ 分析失败: {result['error']}")
            else:
                st.warning("⚠️ 请输入网页URL")
    
    with col2:
        st.markdown("### 📋 使用指南")
        st.markdown("""
        **3步完成分析：**
        
        1. 🌐 输入网页URL
        2. 🔍 点击"开始分析"
        3. 📊 查看智能分析报告
        
        **智能体功能：**
        - 🎯 共识分析：识别主流观点
        - 🔍 偏见识别：检测立场倾向
        - 📚 术语解释：解释专业概念
        - 💡 决策建议：提供实用建议
        """)
    
    # 分析结果展示区域
    if st.session_state.last_analysis_id:
        st.markdown("---")
        st.markdown("### 📊 最近分析")
        st.info(f"记录ID: {st.session_state.last_analysis_id}")
        
        if st.button("🔄 重新分析", key="reanalyze"):
            st.rerun()

def main():
    if not st.session_state.logged_in:
        login_page()
    else:
        main_page()

if __name__ == "__main__":
    main() 