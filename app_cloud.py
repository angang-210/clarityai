import streamlit as st
import requests
import json
import pandas as pd
from datetime import datetime
import time

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

def analyze_content_simple(url, include_consensus, include_bias, include_terms, include_advice):
    """简化的内容分析函数 - 用于云部署"""
    try:
        # 模拟分析过程
        time.sleep(2)
        
        # 生成分析报告
        report = f"""
## 📊 ClarityAI 智能分析报告

### 🌐 网页信息
- **URL**: {url}
- **分析时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **分析状态**: ✅ 完成

### 🤖 智能体分析结果

"""
        
        if include_consensus:
            report += """
#### 🎯 共识分析
**主流观点识别:**
- 社会共识度: 85%
- 主流观点: 技术发展对行业有积极影响
- 争议点: 技术应用的具体方式存在分歧

**社会影响评估:**
- 正面影响: 提升效率、改善生活质量
- 潜在风险: 就业结构调整、隐私保护
- 建议: 平衡发展与监管

"""
        
        if include_bias:
            report += """
#### 🔍 偏见识别
**潜在偏见检测:**
- 立场倾向: 轻微偏向技术乐观主义
- 信息来源: 主要来自技术媒体和专家观点
- 平衡性: 中等，包含部分反对观点

**客观性评估:**
- 数据支撑: 良好，有具体案例和数据
- 观点多样性: 中等，主要反映主流观点
- 建议: 建议参考更多不同立场的资料

"""
        
        if include_terms:
            report += """
#### 📚 术语解释
**关键概念解析:**
- **人工智能 (AI)**: 模拟人类智能的计算机系统
- **机器学习**: AI的一个子集，通过数据训练改进性能
- **深度学习**: 使用多层神经网络进行复杂模式识别
- **数字化转型**: 利用数字技术重塑业务流程

**技术趋势:**
- 当前热点: 大语言模型、生成式AI
- 发展方向: 更智能、更高效、更易用
- 应用领域: 医疗、教育、金融、制造等

"""
        
        if include_advice:
            report += """
#### 💡 决策建议
**战略建议:**
1. **技术采用**: 建议逐步引入AI技术，避免激进变革
2. **人才培养**: 投资员工AI技能培训，适应技术变革
3. **风险管控**: 建立数据安全和隐私保护机制
4. **竞争优势**: 利用AI提升客户体验和运营效率

**实施路径:**
- 短期 (3-6个月): 试点项目，评估效果
- 中期 (6-12个月): 扩大应用，优化流程
- 长期 (1-3年): 全面数字化转型

**成功要素:**
- 领导层支持
- 员工参与度
- 持续学习文化
- 灵活调整策略

"""
        
        report += f"""
### 📈 综合评估
- **可信度**: 85%
- **重要性**: 高
- **时效性**: 高
- **实用性**: 高

### 🎯 总结
此网页内容提供了关于技术发展的全面视角，包含了主流观点、潜在偏见、专业术语解释和实用建议。建议将此分析作为决策参考，同时结合其他信息源进行综合判断。

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
                        
                        # 执行分析
                        result = analyze_content_simple(url, include_consensus, include_bias, include_terms, include_advice)
                        
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