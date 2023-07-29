// Just until Amazon adds a clear size and total cost to the lists.
// First scroll all the way down, then use this script.
// TODO: maybe split priceText by spaces, pick the first (fix euro).
var priceElements = [...document.querySelectorAll('.a-row > * > div.price-section > span.a-price')]
var totalPrice = priceElements
  .map(
    e => {
      const priceText = e.innerText
      const price = priceText
        .split('\n')[0]
        .replace('€', '')
        .replace('.', ',')
        .trim()
      if (price !== "")
        return parseFloat(price)
      return 0.0
    }
  )
  .reduce((accum, val) => {
    return accum + val
  }, 0)
console.log(`This list has ${priceElements.length} items, with a total cost of € ${totalPrice}`)
