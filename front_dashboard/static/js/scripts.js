const fetchData = async (url) => {
    const response = await fetch(url);
    return await response.json();
};

// Initialize Statistics Map
const initStatisticsMap = async () => {
    const query = document.getElementById('query').value;
    const locationType = document.getElementById('locationType').value || 'region';
    const limit = document.getElementById('limit').value || 5;
    const startYear = document.getElementById('startYear').value;
    const endYear = document.getElementById('endYear').value;
    const startMonth = document.getElementById('startMonth').value;
    const endMonth = document.getElementById('endMonth').value;

    const baseUrl = `http://localhost:5000/api/statistics/${query}`;
    const queryString = new URLSearchParams({
        locationType,
        limit,
        startYear,
        endYear,
        startMonth,
        endMonth
    }).toString();
    const url = `${baseUrl}?${queryString}`;

    const { map_html } = await fetchData(url);
    const mapContainer = document.getElementById('statisticsMapContainer');
    mapContainer.innerHTML = map_html.startsWith("data:image/png;base64")
        ? `<img src="${map_html}" style="width:100%; height:auto;" />`
        : map_html;
};

// Initialize Textual Search Map
const initTextualSearch = async () => {
    const keyword = document.getElementById('keyword').value;
    const searchType = document.getElementById('searchType').value;
    const limit = document.getElementById('limitText').value || 5;
    const startYear = document.getElementById('startYearText').value;
    const endYear = document.getElementById('endYearText').value;
    const startMonth = document.getElementById('startMonthText').value;
    const endMonth = document.getElementById('endMonthText').value;

    const url = `http://localhost:5000/api/search/${searchType}?keyword=${encodeURIComponent(keyword)}&limit=${limit}&startYear=${startYear}&endYear=${endYear}&startMonth=${startMonth}&endMonth=${endMonth}`;
    const { map_html } = await fetchData(url);
    const mapContainer = document.getElementById('textSearchMapContainer');
    mapContainer.innerHTML = map_html.startsWith("data:image/png;base64")
        ? `<img src="${map_html}" style="width:100%; height:auto;" />`
        : map_html;
};
