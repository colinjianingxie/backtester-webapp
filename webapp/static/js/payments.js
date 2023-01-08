console.log("Sanity check!");

// Get Stripe publishable key
fetch("config/")
.then((result) => { return result.json(); })
.then((data) => {
  // Initialize Stripe.js
  const stripe = Stripe(data.publicKey);

  // new
  // Event handler
  const checkoutBtns = document.querySelectorAll("[id^='checkout-btn-']");
  checkoutBtns.forEach(cbtn => cbtn.addEventListener("click", (e) => {
      const priceId = e.target.getAttribute("price-id")
      // Get Checkout Session ID
      fetch("create-checkout-session/" + priceId)
      .then((result) => { return result.json(); })
      .then((data) => {
        //console.log(data);
        // Redirect to Stripe Checkout
        return stripe.redirectToCheckout({sessionId: data.sessionId})
      })
      .then((res) => {
        console.log(res);
      });
  }));
});
