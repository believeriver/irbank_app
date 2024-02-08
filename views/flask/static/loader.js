// ページが完全に読み込まれた後にコンテンツを表示
window.addEventListener('load', function() {
    // ローダーを非表示にする
    document.getElementById('loader').style.display = 'none';
    // コンテンツを表示する
    document.getElementById('content').style.display = 'block';
});