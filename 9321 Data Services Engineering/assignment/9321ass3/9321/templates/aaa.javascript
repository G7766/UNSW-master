var radarChartData = {
    labels: ["星期一", "星期二", "星期三", "星期四", "星期五","星期六","星期日"],
    datasets: [
        {
            pointBackgroundColor:'rgba(255, 99, 132, 0.2)',,//描点颜色
            backgroundColor:'rgba(255, 99, 132, 0.2)',//描点背景颜色
            borderColor:'rgba(255, 99, 132, 0.2)',//画线颜色
            data: [15,25,35,45,55,65,75]
        }
        ,
        {
            pointBackgroundColor:'rgba(54, 162, 235, 0.2)',//描点颜色
            backgroundColor:'rgba(54, 162, 235, 0.2)',//描点背景颜色
            borderColor:'rgba(54, 162, 235, 0.2)',//画线颜色
            data: [33,40,5,66,40,77,90]
        }
        ]
    };
var ctx = document.getElementById('mychart').getContext('2d');
var myRadarChart = new Chart(ctx,{type: 'radar',data: radarChartData});