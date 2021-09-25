// Moves the hide button to the first position of child elements, so that you can click to hide entries without moving your mouse
for (const subtext of $$('.subtext')) {
  const children = [...subtext.children]
  const hide = children.find(child => child.text === 'hide')
  if (hide) {
    subtext.removeChild(hide)
    subtext.prepend(hide)
  }
}
