// Just until Amazon adds a clear size and total cost to the lists.
// First scroll all the way down, then use this script.
var priceElements = [...document.querySelectorAll('span.a-price')]
var totalPrice = priceElements
  .map(
    e => {
      const priceText = e.innerText
      const price = priceText
        .split('\n')[0]
        .replace('€', '')
        .replace('.', ',')
        .trim()
      return parseFloat(price)
    }
  )
  .reduce((accum, val) => {
    return accum + val
  }, 0)
console.log(`This list has ${priceElements.length} items, with a total cost of € ${totalPrice}`)
