// collapse all comments, so that it's possible to expand each one individually to read the threads, then collapse it again
[...document.getElementsByTagName('td')]
  .filter(td => td.getAttribute('class') && td.getAttribute('class').includes('ind'))
  .filter(td => td.children.length > 0 && td.children[0].tagName.toLowerCase() === 'img' && td.children[0].getAttribute('width') === '0')
  .forEach(td => {
    const tr = td.parentElement
    const tdWithToggle = [...tr.children].find(td => td.getAttribute('class').includes('default'))
    const stack = []
    stack.push(tdWithToggle)
    let elem = null
    while(stack.length > 0) {
      elem = stack.pop()
      if (!elem) continue
      const clazz = elem.getAttribute('class')
      if (clazz && clazz.includes('comhead')) {
        break
      }
      if (elem.children.length > 0) {
        stack.push(...elem.children)
      }
    }
    if (elem) {
      const toggle = [...elem.children].find(child => {
        return child.getAttribute('class') && child.getAttribute('class').includes('togg')
      })
      if (!toggle.innerText.includes('more')) {
        toggle.click()
      }
    }
  })
;
