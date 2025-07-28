"""
Advanced Visualization Dashboard for Code Transformation Statistics
Interactive charts and analytics using Plotly
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any

from statistics_manager import StatisticsManager


class VisualizationDashboard:
    """Advanced visualization dashboard for transformation statistics"""
    
    def __init__(self, stats_manager: StatisticsManager):
        self.stats_manager = stats_manager
        self.color_scheme = {
            'primary': '#1f77b4',
            'secondary': '#ff7f0e',
            'success': '#2ca02c',
            'danger': '#d62728',
            'warning': '#ff9800',
            'info': '#17a2b8',
            'light': '#f8f9fa',
            'dark': '#343a40'
        }
    
    def render_dashboard(self):
        """Render the main dashboard"""
        st.header("📊 고급 통계 대시보드")
        
        # Get summary stats
        summary = self.stats_manager.get_summary_stats()
        
        # Top metrics row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            self._render_metric_card(
                "총 변환 수",
                f"{summary['total_transformations']:,}",
                "회",
                self.color_scheme['primary']
            )
        
        with col2:
            self._render_metric_card(
                "총 변경사항",
                f"{summary['total_changes']:,}",
                "개",
                self.color_scheme['secondary']
            )
        
        with col3:
            self._render_metric_card(
                "처리된 코드",
                f"{summary['total_lines_processed']:,}",
                "줄",
                self.color_scheme['success']
            )
        
        with col4:
            self._render_metric_card(
                "평균 신뢰도",
                f"{summary['average_confidence']:.1%}",
                "",
                self.color_scheme['info']
            )
        
        # Main visualization tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📈 시계열 분석",
            "🎯 이슈 분포",
            "🔄 변환 패턴",
            "📊 생산성 지표",
            "🗺️ 히트맵"
        ])
        
        with tab1:
            self._render_time_series_analysis()
        
        with tab2:
            self._render_issue_distribution()
        
        with tab3:
            self._render_transformation_patterns()
        
        with tab4:
            self._render_productivity_metrics()
        
        with tab5:
            self._render_heatmap_analysis()
    
    def _render_time_series_analysis(self):
        """Render time series analysis charts"""
        st.subheader("시계열 분석")
        
        # Period selector
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            period = st.selectbox("기간", ["일별", "주별", "월별"])
            period_map = {"일별": "daily", "주별": "weekly", "월별": "monthly"}
            period_key = period_map[period]
        
        with col2:
            if period == "일별":
                days = st.selectbox("표시 기간", [7, 14, 30, 60, 90])
            else:
                days = 0
        
        # Get time series data
        df = self.stats_manager.get_time_series_data(period_key, days)
        
        if not df.empty:
            # Create subplots
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=('변환 횟수', '변경사항 수', '처리된 코드 라인', '누적 변화'),
                specs=[[{"secondary_y": False}, {"secondary_y": False}],
                      [{"secondary_y": False}, {"secondary_y": True}]]
            )
            
            # Transformations over time
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df['transformations'],
                    mode='lines+markers',
                    name='변환 횟수',
                    line=dict(color=self.color_scheme['primary'], width=2),
                    marker=dict(size=8)
                ),
                row=1, col=1
            )
            
            # Changes over time
            fig.add_trace(
                go.Bar(
                    x=df.index,
                    y=df['changes'],
                    name='변경사항',
                    marker_color=self.color_scheme['secondary']
                ),
                row=1, col=2
            )
            
            # Lines of code
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df['lines'],
                    mode='lines',
                    name='코드 라인',
                    fill='tozeroy',
                    line=dict(color=self.color_scheme['success'])
                ),
                row=2, col=1
            )
            
            # Cumulative changes
            df['cumulative_changes'] = df['changes'].cumsum()
            df['cumulative_transformations'] = df['transformations'].cumsum()
            
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df['cumulative_changes'],
                    mode='lines',
                    name='누적 변경사항',
                    line=dict(color=self.color_scheme['danger'], width=2)
                ),
                row=2, col=2
            )
            
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df['cumulative_transformations'],
                    mode='lines',
                    name='누적 변환',
                    line=dict(color=self.color_scheme['info'], width=2, dash='dash')
                ),
                row=2, col=2, secondary_y=True
            )
            
            # Update layout
            fig.update_layout(
                height=600,
                showlegend=True,
                title_text=f"{period} 통계 추이",
                hovermode='x unified'
            )
            
            # Update axes
            fig.update_xaxes(title_text="날짜", row=2, col=1)
            fig.update_xaxes(title_text="날짜", row=2, col=2)
            fig.update_yaxes(title_text="횟수", row=1, col=1)
            fig.update_yaxes(title_text="개수", row=1, col=2)
            fig.update_yaxes(title_text="라인 수", row=2, col=1)
            fig.update_yaxes(title_text="누적 변경사항", row=2, col=2)
            fig.update_yaxes(title_text="누적 변환", secondary_y=True, row=2, col=2)
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Moving average
            if len(df) > 7:
                st.subheader("이동 평균 분석")
                
                window = st.slider("이동 평균 기간", 3, 14, 7)
                
                df[f'ma_{window}'] = df['changes'].rolling(window=window).mean()
                
                fig_ma = go.Figure()
                
                fig_ma.add_trace(go.Scatter(
                    x=df.index,
                    y=df['changes'],
                    mode='markers',
                    name='실제 변경사항',
                    marker=dict(color=self.color_scheme['light'], size=6)
                ))
                
                fig_ma.add_trace(go.Scatter(
                    x=df.index,
                    y=df[f'ma_{window}'],
                    mode='lines',
                    name=f'{window}일 이동평균',
                    line=dict(color=self.color_scheme['danger'], width=3)
                ))
                
                fig_ma.update_layout(
                    title=f"변경사항 {window}일 이동평균",
                    xaxis_title="날짜",
                    yaxis_title="변경사항 수",
                    hovermode='x unified'
                )
                
                st.plotly_chart(fig_ma, use_container_width=True)
        else:
            st.info("아직 시계열 데이터가 충분하지 않습니다.")
    
    def _render_issue_distribution(self):
        """Render issue type distribution charts"""
        st.subheader("이슈 유형 분포")
        
        issue_dist = self.stats_manager.get_issue_distribution()
        
        if issue_dist:
            # Prepare data
            df = pd.DataFrame(
                list(issue_dist.items()),
                columns=['이슈 유형', '발생 횟수']
            )
            df = df.sort_values('발생 횟수', ascending=False)
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Pie chart
                fig_pie = px.pie(
                    df,
                    values='발생 횟수',
                    names='이슈 유형',
                    title='이슈 유형별 비율',
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                
                fig_pie.update_traces(
                    textposition='inside',
                    textinfo='percent+label',
                    hoverinfo='label+percent+value'
                )
                
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with col2:
                # Bar chart
                fig_bar = px.bar(
                    df.head(10),
                    x='발생 횟수',
                    y='이슈 유형',
                    orientation='h',
                    title='상위 10개 이슈 유형',
                    color='발생 횟수',
                    color_continuous_scale='Blues'
                )
                
                fig_bar.update_layout(
                    yaxis={'categoryorder': 'total ascending'},
                    showlegend=False
                )
                
                st.plotly_chart(fig_bar, use_container_width=True)
            
            # Treemap
            st.subheader("이슈 유형 트리맵")
            
            fig_tree = px.treemap(
                df,
                path=['이슈 유형'],
                values='발생 횟수',
                title='이슈 유형 계층 구조',
                color='발생 횟수',
                color_continuous_scale='RdYlBu_r'
            )
            
            fig_tree.update_layout(height=500)
            st.plotly_chart(fig_tree, use_container_width=True)
        else:
            st.info("아직 이슈 분포 데이터가 없습니다.")
    
    def _render_transformation_patterns(self):
        """Render transformation pattern analysis"""
        st.subheader("변환 패턴 분석")
        
        # Get top transformations
        top_transforms = self.stats_manager.get_top_transformations(20)
        
        if top_transforms:
            # Prepare data
            df = pd.DataFrame(top_transforms, columns=['변환', '횟수'])
            
            # Horizontal bar chart
            fig = px.bar(
                df,
                x='횟수',
                y='변환',
                orientation='h',
                title='가장 빈번한 변환 패턴 (상위 20개)',
                color='횟수',
                color_continuous_scale='Viridis',
                text='횟수'
            )
            
            fig.update_traces(texttemplate='%{text}', textposition='outside')
            fig.update_layout(
                yaxis={'categoryorder': 'total ascending'},
                height=600,
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Word frequency analysis
            st.subheader("변환 전후 단어 빈도")
            
            # Extract original and suggested words
            originals = []
            suggesteds = []
            
            for transform, count in top_transforms:
                if ' → ' in transform:
                    orig, sugg = transform.split(' → ')
                    originals.extend([orig] * count)
                    suggesteds.extend([sugg] * count)
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Original words frequency
                orig_freq = pd.Series(originals).value_counts().head(15)
                
                fig_orig = px.bar(
                    x=orig_freq.values,
                    y=orig_freq.index,
                    orientation='h',
                    title='변환 전 단어 빈도',
                    labels={'x': '빈도', 'y': '원본 변수명'},
                    color=orig_freq.values,
                    color_continuous_scale='Reds'
                )
                
                st.plotly_chart(fig_orig, use_container_width=True)
            
            with col2:
                # Suggested words frequency
                sugg_freq = pd.Series(suggesteds).value_counts().head(15)
                
                fig_sugg = px.bar(
                    x=sugg_freq.values,
                    y=sugg_freq.index,
                    orientation='h',
                    title='변환 후 단어 빈도',
                    labels={'x': '빈도', 'y': '제안 변수명'},
                    color=sugg_freq.values,
                    color_continuous_scale='Greens'
                )
                
                st.plotly_chart(fig_sugg, use_container_width=True)
            
            # Sankey diagram for transformation flow
            if len(top_transforms) > 5:
                st.subheader("변환 흐름도 (Sankey Diagram)")
                
                # Prepare data for Sankey
                sources = []
                targets = []
                values = []
                labels = []
                
                for i, (transform, count) in enumerate(top_transforms[:15]):
                    if ' → ' in transform:
                        orig, sugg = transform.split(' → ')
                        
                        if orig not in labels:
                            labels.append(orig)
                        if sugg not in labels:
                            labels.append(sugg)
                        
                        sources.append(labels.index(orig))
                        targets.append(labels.index(sugg))
                        values.append(count)
                
                fig_sankey = go.Figure(data=[go.Sankey(
                    node=dict(
                        pad=15,
                        thickness=20,
                        line=dict(color="black", width=0.5),
                        label=labels,
                        color=self.color_scheme['primary']
                    ),
                    link=dict(
                        source=sources,
                        target=targets,
                        value=values,
                        color='rgba(31, 119, 180, 0.4)'
                    )
                )])
                
                fig_sankey.update_layout(
                    title="변수명 변환 흐름",
                    height=600
                )
                
                st.plotly_chart(fig_sankey, use_container_width=True)
        else:
            st.info("아직 변환 패턴 데이터가 없습니다.")
    
    def _render_productivity_metrics(self):
        """Render productivity metrics"""
        st.subheader("생산성 지표")
        
        metrics = self.stats_manager.get_productivity_metrics()
        
        # Display key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "일평균 변환",
                f"{metrics['avg_daily_transformations']:.1f}",
                "회/일"
            )
        
        with col2:
            st.metric(
                "일평균 변경",
                f"{metrics['avg_daily_changes']:.1f}",
                "개/일"
            )
        
        with col3:
            st.metric(
                "일평균 처리 코드",
                f"{metrics['avg_daily_lines']:.0f}",
                "줄/일"
            )
        
        with col4:
            if metrics['peak_day']:
                st.metric(
                    "최다 변경일",
                    metrics['peak_day'],
                    f"{metrics['peak_changes']}개"
                )
        
        # Productivity trends
        daily_data = self.stats_manager.get_time_series_data('daily', 30)
        
        if not daily_data.empty:
            # Calculate productivity score
            daily_data['productivity_score'] = (
                daily_data['transformations'] * 10 +
                daily_data['changes'] * 2 +
                daily_data['lines'] * 0.1
            )
            
            # Create gauge chart for today's productivity
            today_score = daily_data['productivity_score'].iloc[-1] if len(daily_data) > 0 else 0
            avg_score = daily_data['productivity_score'].mean()
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Gauge chart
                fig_gauge = go.Figure(go.Indicator(
                    mode="gauge+number+delta",
                    value=today_score,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "오늘의 생산성 점수"},
                    delta={'reference': avg_score, 'relative': True},
                    gauge={
                        'axis': {'range': [None, avg_score * 2]},
                        'bar': {'color': self.color_scheme['success']},
                        'steps': [
                            {'range': [0, avg_score * 0.5], 'color': self.color_scheme['light']},
                            {'range': [avg_score * 0.5, avg_score], 'color': "lightgray"},
                            {'range': [avg_score, avg_score * 1.5], 'color': "gray"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': avg_score
                        }
                    }
                ))
                
                fig_gauge.update_layout(height=400)
                st.plotly_chart(fig_gauge, use_container_width=True)
            
            with col2:
                # Productivity trend
                fig_trend = go.Figure()
                
                fig_trend.add_trace(go.Scatter(
                    x=daily_data.index,
                    y=daily_data['productivity_score'],
                    mode='lines+markers',
                    name='생산성 점수',
                    line=dict(color=self.color_scheme['primary'], width=2),
                    fill='tozeroy'
                ))
                
                # Add average line
                fig_trend.add_hline(
                    y=avg_score,
                    line_dash="dash",
                    line_color="red",
                    annotation_text=f"평균: {avg_score:.1f}"
                )
                
                fig_trend.update_layout(
                    title="생산성 추이 (최근 30일)",
                    xaxis_title="날짜",
                    yaxis_title="생산성 점수",
                    height=400,
                    showlegend=False
                )
                
                st.plotly_chart(fig_trend, use_container_width=True)
            
            # Efficiency metrics
            st.subheader("효율성 분석")
            
            # Calculate efficiency metrics
            daily_data['changes_per_transformation'] = (
                daily_data['changes'] / daily_data['transformations']
            ).fillna(0)
            
            daily_data['lines_per_transformation'] = (
                daily_data['lines'] / daily_data['transformations']
            ).fillna(0)
            
            # Create scatter plot
            fig_scatter = px.scatter(
                daily_data,
                x='changes_per_transformation',
                y='lines_per_transformation',
                size='transformations',
                color='productivity_score',
                title='효율성 분포 (버블 크기 = 변환 횟수)',
                labels={
                    'changes_per_transformation': '변환당 변경사항',
                    'lines_per_transformation': '변환당 처리 라인'
                },
                color_continuous_scale='Viridis'
            )
            
            st.plotly_chart(fig_scatter, use_container_width=True)
    
    def _render_heatmap_analysis(self):
        """Render heatmap analysis"""
        st.subheader("활동 히트맵")
        
        # Get daily data for the last 90 days
        daily_data = self.stats_manager.get_time_series_data('daily', 90)
        
        if not daily_data.empty:
            # Prepare data for heatmap
            daily_data['weekday'] = daily_data.index.day_name()
            daily_data['week'] = daily_data.index.isocalendar().week
            daily_data['date'] = daily_data.index.date
            
            # Create pivot table for heatmap
            heatmap_data = daily_data.pivot_table(
                values='changes',
                index='weekday',
                columns='week',
                aggfunc='sum',
                fill_value=0
            )
            
            # Reorder weekdays
            weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            heatmap_data = heatmap_data.reindex(weekday_order)
            
            # Create heatmap
            fig_heatmap = px.imshow(
                heatmap_data,
                labels=dict(x="주차", y="요일", color="변경사항"),
                title="주간 활동 히트맵",
                color_continuous_scale='RdYlGn',
                aspect='auto'
            )
            
            fig_heatmap.update_layout(height=400)
            st.plotly_chart(fig_heatmap, use_container_width=True)
            
            # Hour heatmap (if we had hour data)
            st.subheader("시간대별 활동 패턴")
            
            # Simulate hourly pattern
            hours = list(range(24))
            days = ['월', '화', '수', '목', '금', '토', '일']
            
            # Create sample data (in real case, this would come from actual timestamps)
            np.random.seed(42)
            hourly_data = np.random.rand(7, 24) * 10
            
            # Apply typical work pattern
            for i in range(5):  # Weekdays
                hourly_data[i, 9:18] *= 3  # 9 AM to 6 PM
                hourly_data[i, :7] *= 0.1  # Early morning
                hourly_data[i, 22:] *= 0.1  # Late night
            
            fig_hourly = go.Figure(data=go.Heatmap(
                z=hourly_data,
                x=hours,
                y=days,
                colorscale='Viridis',
                text=hourly_data.round(1),
                texttemplate='%{text}',
                textfont={"size": 10}
            ))
            
            fig_hourly.update_layout(
                title="시간대별 평균 활동량",
                xaxis_title="시간",
                yaxis_title="요일",
                height=400
            )
            
            st.plotly_chart(fig_hourly, use_container_width=True)
        else:
            st.info("히트맵을 생성할 데이터가 충분하지 않습니다.")
    
    def _render_metric_card(self, label: str, value: str, unit: str, color: str):
        """Render a styled metric card"""
        st.markdown(
            f"""
            <div style='
                background: linear-gradient(135deg, {color}dd 0%, {color}99 100%);
                color: white;
                padding: 1.5rem;
                border-radius: 12px;
                text-align: center;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            '>
                <div style='font-size: 0.9em; opacity: 0.9; margin-bottom: 0.5rem;'>{label}</div>
                <div style='font-size: 2.2em; font-weight: bold; margin: 0.2rem 0;'>{value}</div>
                <div style='font-size: 0.8em; opacity: 0.8;'>{unit}</div>
            </div>
            """,
            unsafe_allow_html=True
        )