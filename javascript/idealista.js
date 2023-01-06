/**
 * Sleep for some ms...
 * From: https://www.sitepoint.com/delay-sleep-pause-wait/
 */
function sleep(milliseconds) {
  const date = Date.now();
  let currentDate = null;
  do {
    currentDate = Date.now();
  } while (currentDate - date < milliseconds);
}

// Fetch all the ads on the page
var ads = document.querySelectorAll('.item')
console.log(`This page has ${ads.length} ads`)

var floorRegex = /planta 1ª/i

var neighborhoods = ['raval', 'gotic', 'gothic', 'gótic', 'gòtic' , 'poble sec', 'poblesec', 'poble nou', 'poblenou']

for (const ad of ads) {
  const floor = ad.querySelector('div.item-detail-char').children[2].textContent
  if (floor.match(floorRegex)) {
    console.log(`This ad is on ${floor} floor. Say bye-bye to it.`)
    const trashButton = ad.querySelector('.trash-btn')
    trashButton.click()
    sleep(500)
    continue
  }
  if (floor.toLowerCase().indexOf('sin ascensor') >= 0) {
    console.log('This piso lied that it had ascensor. Say bye-bye to it.')
    const trashButton = ad.querySelector('.trash-btn')
    trashButton.click()
    sleep(500)
    continue
  }
  const neighborhood = ad.querySelector('.item-link').textContent
  for (const n of neighborhoods) {
    if (neighborhood.toLowerCase().indexOf(n) >= 0) {
      console.log(`This ad is located at ${n} neighborhood. Say bye-bye to it.`)
      const trashButton = ad.querySelector('.trash-btn')
      trashButton.click()
      sleep(500)
      continue
    }
  }
}
