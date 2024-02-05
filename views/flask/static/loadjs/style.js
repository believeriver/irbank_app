<script>
$(function() {
  var h = $(window).height();

  $('#wrap').css('display','none');
  $('#loading ,#spinner').height(h).css('display','block');
});

$(window).on('load',function () {
  $('#wrap').css('display', 'block');
  $('#loading').delay(500).fadeOut(500);
  $('#spinner').delay(300).fadeOut(300);
});

//5秒たったら強制的にロード画面を非表示
$(function(){
  setTimeout('stopload()',5000);
});

function stopload(){
  $('#wrap').css('display','block');
  $('#loading').delay(500).fadeOut(500);
  $('#spinner').delay(300).fadeOut(300);
}

</script>