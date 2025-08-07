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
</style>
""", unsafe_allow_html=True)

# 初始化session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

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
    </div>
    """, unsafe_allow_html=True)
    
    # 侧边栏
    with st.sidebar:
        st.markdown("### 🛠️ 功能菜单")
        
        if st.button("🚪 退出登录"):
            st.session_state.logged_in = False
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 📊 系统信息")
        st.info(f"当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        st.info("状态: 正常运行")
    
    # 主要内容
    st.markdown("### 🌐 网页内容分析")
    
    # URL输入
    url = st.text_input("请输入网页URL", placeholder="https://example.com")
    
    if st.button("🔍 开始分析", type="primary"):
        if url:
            with st.spinner("正在分析网页内容..."):
                # 模拟分析过程
                time.sleep(2)
                
                # 显示分析结果
                st.success("✅ 分析完成！")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### 📊 内容概览")
                    st.info("网页类型: 新闻资讯")
                    st.info("主要内容: 科技新闻")
                    st.info("情感倾向: 中性")
                
                with col2:
                    st.markdown("### 🤖 AI解读")
                    st.success("可信度: 85%")
                    st.success("重要性: 中等")
                    st.success("时效性: 高")
                
                st.markdown("### 📝 详细分析")
                st.markdown("""
                这是一个关于科技发展的新闻网页，内容主要涉及：
                - 技术创新
                - 行业趋势
                - 市场动态
                
                **AI建议：**
                - 内容可信度较高
                - 建议关注相关技术发展
                - 可以作为决策参考
                """)
        else:
            st.warning("⚠️ 请输入网页URL")

def main():
    if not st.session_state.logged_in:
        login_page()
    else:
        main_page()

if __name__ == "__main__":
    main() 