//轮播图效果
var indicator_ul = document.querySelector('.entry .container .indicator');
var lis2 = document.querySelectorAll('.entry .container .banner li');
for (var i = 0; i < lis2.length; i++) {
  var li = document.createElement('li');
  if (i === 0) {
    li.classList.add('active');
  }
  indicator_ul.appendChild(li);
}
var lis1=indicator_ul.querySelectorAll('li');
var index = 0;


function updateCarousel() {
  lis2.forEach((li, i) => li.style.display = i === index ? 'block' : 'none');
  lis1.forEach((li, i) => i === index ? li.classList.add('active') : li.classList.remove('active'));
}

var timer = setInterval(function() {
  index = (index + 1) % lis2.length;
  updateCarousel();
}, 3000);

function handleArrowClick(direction) {
  index = (index + direction + lis2.length) % lis2.length;
  updateCarousel();
}

var prev = document.querySelector('.entry .container .prevArrow');
var next = document.querySelector('.entry .container .nextArrow');

prev.addEventListener('click', () => handleArrowClick(-1));
prev.addEventListener('mouseenter', () => prev.style.display = 'block');
prev.addEventListener('mouseleave', () => prev.style.display = 'none');
next.addEventListener('click', () => handleArrowClick(1));
next.addEventListener('mouseenter', () => next.style.display = 'block');
next.addEventListener('mouseleave', () => next.style.display = 'none');

if (lis1.length > 0 && lis2.length > 0) {
  lis1.forEach((li, i) => {
    li.setAttribute('index', i);
    li.addEventListener('click', function() {
      index = parseInt(this.getAttribute('index'), 10);
      updateCarousel();
    });
  });
} else {
  console.error('Banner or indicator list items not found.');
}

//轮播图效果结束,当鼠标移入图片时，停止ousel定时器，鼠标移出图片时，开启ousel定时器
lis2.forEach(li => {
  li.addEventListener('mouseenter', function() {
    clearInterval(timer);
    prev.style.display = 'block';
    next.style.display = 'block';
  });
  li.addEventListener('mouseleave', function() {
    timer = setInterval(function() {
      index = (index + 1) % lis2.length;
      updateCarousel();
    }, 3000);
    prev.style.display = 'none';
    next.style.display = 'none';
  });
  
});
