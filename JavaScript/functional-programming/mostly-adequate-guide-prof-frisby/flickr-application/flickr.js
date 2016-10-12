/* globals requirejs */

/**
 * Get a bunch of images matching a particular tag from the flickr api and
 * render them on the DOM.
 */
requirejs.config({
  paths: {
    ramda: 'https://cdnjs.cloudflare.com/ajax/libs/ramda/0.13.0/ramda.min',
    jquery: 'https://ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min'
  }
});

require([
  'ramda', 'jquery'
], (_, $) => {
  // eslint-disable-next-line no-console, no-unused-vars
  const trace = _.curry((tag, x) => !console.log(tag, x) && x);

  const Impure = {
    getJSON: _.curry((callback, url) => {
      $.getJSON(url, callback);
    }),

    setHTML: _.curry((sel, html) => {
      $(sel).html(html);
    })
  };

  const url = term =>
    `https://api.flickr.com/services/feeds/photos_public.gne?tags=${
      term}&format=json&jsoncallback=?`;

  const mediaUrl = _.compose(_.prop('m'), _.prop('media'));

  const image = src => $('<img />', { src });

  // map's composition law: compose(map(f), map(g)) == map(compose(f, g))
  const mediaToImg = _.compose(image, mediaUrl);
  const images = _.compose(_.map(mediaToImg), _.prop('items'));

  const renderImages = _.compose(Impure.setHTML('body'), images);

  const app = _.compose(Impure.getJSON(renderImages), url);

  app('cats');
});
