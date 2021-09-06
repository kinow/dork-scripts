$$("[data-hook='product-item-out-of-stock']").forEach(span => {
  span.parentElement.parentElement.parentElement.remove()
})
