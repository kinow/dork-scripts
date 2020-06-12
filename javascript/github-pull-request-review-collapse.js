// Collapses all files in a GitHub pull request (useful when reviewing changes with 100+ files)

[...document.getElementsByClassName("Details-content--shown")]
  .filter(e => {
    const parent = e.parentElement
    return parent.getAttribute('aria-expanded') === "true"
  })
  .map((e) => {
    e.parentElement.click()
  })
;


// Mark all files as viewed in a GitHub pull request (useful when reviewing changes with 100+ files)

[...document.getElementsByTagName('input')]
  .filter(e => e.getAttribute('type') === 'checkbox' && e.getAttribute('name') === 'viewed')
  .filter(e => e.getAttribute('data-ga-click').replaceAll(' ', '').includes('value:false'))
  .map(e => e.click())
;
