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

// For a FFox bookmark:
//
// javascript:(function()%7B%5B...(document.getElementById(%22stories%22).children)%5D.filter(e%20%3D%3E%20e.tagName.toLowerCase()%20%3D%3D%3D%20%27div%27).filter((e)%20%3D%3E%20%7Bconst%20images%20%3D%20%5B...(e.querySelectorAll(%27img%27))%5D%3Bconst%20audioIcon%20%3D%20images.filter((i)%20%3D%3E%20i.title.toLowerCase().includes(%27audio%27))%3Breturn%20audioIcon.length%20%3D%3D%3D%200%7D).map((e)%20%3D%3E%20e.remove())%3B%7D)()%3B%0A
