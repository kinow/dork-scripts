// Moves the hide button to the first position of child elements, so that you can click to hide entries without moving your mouse
for (const comment of $$('.comhead')) {
  const navs = comment.querySelector('.navs')
  const hide = navs.querySelector('.togg')
  navs.removeChild(hide)
  comment.prepend(hide)
}
