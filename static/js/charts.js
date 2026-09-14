/* Chart.js Visualization Helpers for AI & Analytics */

function renderFeatureImportanceChart(canvasId, featureImportanceObj) {
    const ctx = document.getElementById(canvasId);
    if (!ctx || !featureImportanceObj) return;

    const labels = Object.keys(featureImportanceObj);
    const values = Object.values(featureImportanceObj);

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Importance Weight (%)',
                data: values,
                backgroundColor: 'rgba(99, 102, 241, 0.75)',
                borderColor: '#6366f1',
                borderWidth: 1.5,
                borderRadius: 6
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return ` ${context.raw}% influence on recommendation`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    ticks: { color: '#94a3b8' }
                },
                y: {
                    grid: { display: false },
                    ticks: { color: '#f8fafc', font: { weight: 'bold' } }
                }
            }
        }
    });
}

function renderAnalyticsCharts(chartData) {
    if (!chartData) return;

    // 1. Applications by Course
    const courseCtx = document.getElementById('chartCourses');
    if (courseCtx && chartData.courses) {
        new Chart(courseCtx, {
            type: 'bar',
            data: {
                labels: chartData.courses.map(c => c.course.replace('B.Tech ', '')),
                datasets: [{
                    label: 'Applications',
                    data: chartData.courses.map(c => c.count),
                    backgroundColor: '#6366f1',
                    borderRadius: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    x: { ticks: { color: '#94a3b8' } },
                    y: { ticks: { color: '#94a3b8' }, grid: { color: 'rgba(255, 255, 255, 0.05)' } }
                }
            }
        });
    }

    // 2. Eligibility Distribution (Doughnut)
    const eligCtx = document.getElementById('chartEligibility');
    if (eligCtx && chartData.eligibility) {
        new Chart(eligCtx, {
            type: 'doughnut',
            data: {
                labels: chartData.eligibility.map(e => e.label),
                datasets: [{
                    data: chartData.eligibility.map(e => e.count),
                    backgroundColor: ['#10b981', '#ef4444'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'bottom', labels: { color: '#f8fafc' } }
                }
            }
        });
    }

    // 3. AI Recommendation Distribution (Pie)
    const recCtx = document.getElementById('chartRecommendation');
    if (recCtx && chartData.recommendation) {
        new Chart(recCtx, {
            type: 'pie',
            data: {
                labels: chartData.recommendation.map(r => r.label),
                datasets: [{
                    data: chartData.recommendation.map(r => r.count),
                    backgroundColor: ['#10b981', '#6366f1', '#f59e0b', '#ef4444'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'bottom', labels: { color: '#f8fafc' } }
                }
            }
        });
    }

    // 4. Processing Funnel Chart
    const funnelCtx = document.getElementById('chartFunnel');
    if (funnelCtx && chartData.funnel) {
        const f = chartData.funnel;
        new Chart(funnelCtx, {
            type: 'bar',
            data: {
                labels: ['Applications Submitted', 'Documents Uploaded', 'Eligible', 'AI Recommended', 'Officer Approved'],
                datasets: [{
                    label: 'Candidates',
                    data: [f.submitted, f.docs_uploaded, f.eligible, f.ai_recommended, f.officer_approved],
                    backgroundColor: ['#a855f7', '#3b82f6', '#10b981', '#6366f1', '#059669'],
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    x: { ticks: { color: '#94a3b8' } },
                    y: { ticks: { color: '#94a3b8' }, grid: { color: 'rgba(255, 255, 255, 0.05)' } }
                }
            }
        });
    }
}
