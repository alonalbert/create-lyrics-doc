lastToggled=null

function setTranslated(e) {
    e.innerHTML = e.getAttribute("data-translation");
    e.classList.add('translation')
}

function setOriginal(e) {
    e.innerHTML = e.getAttribute("data-text");
    e.classList.remove('translation')
}

function toggle(e) {
  if (lastToggled && lastToggled != e) {
    setOriginal(lastToggled)
    lastToggled =  null
  }
  if (e.innerHTML == e.getAttribute("data-text")) {
    setTranslated(e)
    lastToggled = e
  } else {
    setOriginal(e)
    lastToggled =  null
  }
}

function scrollDown() {
    var content = document.getElementById("content");
    var header = document.getElementById("header");
    content.scrollTop += content.getBoundingClientRect().height - 2 * header.getBoundingClientRect().height;
}

function scrollUp() {
    var content = document.getElementById("content");
    var header = document.getElementById("header");
    content.scrollTop -= content.getBoundingClientRect().height - 2 * header.getBoundingClientRect().height;
}
