// Removes all divs that are missing the audio icon

[...(document.getElementById("stories").children)]
  .filter(e => e.tagName.toLowerCase() === 'div')
  .filter((e) => {
    const images = [...(e.querySelectorAll('img'))];
    const audioIcon = images.filter((i) => i.title.toLowerCase().includes('audio'))
    return audioIcon.length === 0
  })
  .map((e) => e.remove())
;

