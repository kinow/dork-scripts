var TERMS = 'unity,unreal,blender,made with,made on,i used,game engine,github,godot,we used'
TERMS
  .split(',')
  .forEach(w => {
    if (w) {
      // search
      if (window.find(w, 0, 0)) {
        // alert
        console.log(`FOUND ${w}!`)
        throw new Error;
      }
      // scroll down
      // window.scrollByLines(LINES)
    }
  }
)

