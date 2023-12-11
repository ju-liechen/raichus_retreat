function openLink(linkToken, csrfToken) {
    const handler = Plaid.create({
      token: linkToken,
      onSuccess: (public_token, metadata) => {
        htmx.ajax('PUT', '/bank/', {
          values: {'public_token': public_token},
          headers: {'X-CSRFToken': csrfToken},
          target: '#bank-dashboard', 
          swap: 'beforeend'
        })
        htmx.ajax('GET', '/bank/', {
          headers: {'X-CSRFToken': csrfToken},
        });
      },
      onLoad: () => {},
      onExit: (err, metadata) => {
        htmx.ajax('POST', '/clear-link-token/', {
          headers: {'X-CSRFToken': csrfToken},
        });
        htmx.ajax('GET', '/bank/', {
          headers: {'X-CSRFToken': csrfToken},
        });
      },
      onEvent: (eventName, metadata) => {},
    })
    handler.open();
  }