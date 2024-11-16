---
layout: post
title: "Material Design using Veutify and Dependency Injection using Inversify"
date: 2020-02-21
category: Programming
tags: [vue,typescript,vuetify,inversify]
comments: true
featured: true
---
So far the project is pretty ugly.  It's literally a white page with the words lootly on it.  Not really inspiring at all.  Today we'll incorporate some material design using the vuetify library.  Once we  have that out of the way we'll build a component, and some kind of service and start to plugin in the beginning of dependency injection using inversify.

We won't be using the full version of inversify.  Instead there is a cool annotation library that brings the power of dependency injection without us needing all of inversify.

## Dependency Injection Primer

Dependency injection (DI) is a pretty useful concept.  Basically, it lets you create objects that depend on other objects without having to know how to create those other objects.  As an example, eventually in this project we will be creating a component for creating a book definition. In order to save the book we will need a copy of the book service.  We don't need the book component to know how to create the book service; instead by using dependency injection; the DI framework creates the book service for us and "injects" that instance into our book component.

The book service itself might need another object, maybe a configuration service, and so it would need to either know how to create the configuration service or you'd have to pass the configuraiton service into the constructor of the book service.

Here is how the book component might look if it needed to know about the book service and the book service needed the configuration service as part of it's constructor.

```html
<template>
  <div>
    ...
    book form
    ...
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import IBookService from '@/services/IBookService'
import BookService from '@/services/impl/BookService'
import IConfigService from '@/services/IConfigService'
import ConfigurationService from '@/services/impl/ConfigurationService'

@Component({
  name: 'book'
})

export default class extends Vue {
  private configurationService: IConfigService = new ConfigurationService('https://my-api-server.com')
  private bookService : IBookService = new BookService(configurationService)
  ...
}
</script>
```

With dependency injection the book component would look more like this:

```html
<template>
  <div>
    ...
    book form
    ...
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { inject } from 'inversify-props'
import IBookService from '@/services/IBookService'

@Component({
  name: 'book'
})

export default class extends Vue {

  @inject('bookService')
  public bookService!: IBookService
  ...
}
</script>
```

As you can see the entire book component got a lot simpler.

Meanwhile the BookService would be something like this:

```js
import { inject, injectable } from 'inversify-props'

import IBookService from '@/services/IBookService'
import IConfigService from '@/services/IConfigService'


@injectable()
export default class BookService implements IBookService {

  // the bit in the parentheses with the string will be changed in our final implementation so we don't have these magic strings
  // all over the place.  We'll end up with a more robust solution using a "Registry" that I'll explain in the next post.
  @inject('configService')
  public configService!: IConfigService

  ...
}
```

Now the book component doesn't need to know anything about what the BookService needs to do its job.  Pretty slick.

We're not going to get too far into actual usage of Dependency Injection in this step but we are going to set it up so we are ready in the next article.

## Installing the Libraries

For both vuetify (Material Design) and inversify (Dependency Injection) we're going to use npm to install them.  This is pretty straight forward; just issue the following commands from the root directory of your project:

```sh
npm install inversify-props
npm install reflect-metadata
npm install vuetify
npm install --save-dev vue-cli-plugin-vuetify
npm install --save-dev vuetify-loader
```

To be honest, I'm not sure if we totally need the two dev dependencies.  But, they seem like a safe option. All five install pretty quickly the update will impact your package.json and package-lock.json files.  reflect-metadata is used in conjunction with the inversify-props.

They won't actually be available in your project yet though.  In order to enable them you have to go into your `/src/main.ts` file and bootstrap them.

### Setting up Vuetify

Vuetify is a little less work so we'll start with it.

* in your `/src/` directory add a `plugins` directory
* in the `/src/plugins` directory add the file `vuetify.ts` which contains:

  ```js
  import Vue from 'vue'
  import Vuetify from 'vuetify'
  import 'vuetify/dist/vuetify.min.css'

  Vue.use(Vuetify)

  const opts = {}

  export default new Vuetify(opts)
  ```

* edit your `/src/main.ts` file so that it ends up like this:

```js
import Vue from 'vue'
import App from './App.vue'
// the @ is going to be used a lot.  It helps avoid things like ../../../some_directory/some_file.ts
// instead you can do @/some_directory/some_file.ts
import vuetify from '@/plugins/vuetify'

Vue.config.productionTip = false

new Vue({
  vuetify,
  render: h => h(App)
}).$mount('#app')
```

That basically tells Vue to use Vuetify.  Pretty straight forward.

You need the material icons.  There are two choices here.

1. You could install a node module with them and incorporate it.  That works if you can't use the CDN; for example you're in a private network.  However, this will enlarge the overall size of your deployment.
2. You can use the CDN. That's what I'm doing for this demonstration.  To do that you have to edit `/public/index.html`:

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width,initial-scale=1.0">
    <link rel="icon" href="<%= BASE_URL %>favicon.ico">
    <title><%= htmlWebpackPlugin.options.title %></title>

    <link href="https://fonts.googleapis.com/css?family=Roboto:100,300,400,500,700,900" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/@mdi/font@4.x/css/materialdesignicons.min.css" rel="stylesheet">
  </head>
  <body>
    <noscript>
      <strong>We're sorry but <%= htmlWebpackPlugin.options.title %> doesn't work properly without JavaScript enabled. Please enable it to continue.</strong>
    </noscript>
    <div id="app"></div>
    <!-- built files will be auto injected -->
  </body>
</html>
```

The two `<link>` values proide all the fonts and icons you need for the overall *material* feel.

The installation of the node module option would work as follows:

```sh
npm install @mdi/font
```

Plus, updating your `/src/plugins/vuetify.ts` file to include:

```js
import '@mdi/font/css/materialdesignicons.css'
```

Lastly, in order to see the cool material design look and feel I picked the pre-built Vuetify "Google Contacts" layout and updated my `/src/App.vue` to use some of it.

I'm not going to post the entire contents of App.vue - but you can see them and [all of these changes can be seen in this github commit](https://github.com/finalcut/vue-lootly/tree/c7fa8abc4691c773448c6968ae44bc945422f5bf)

## Prepare for Inversification

Next up we are going to add the inversify library, and set up our "dependency injection container".  The "container" basically tells inverisfy how to satisfiy different injection requests.  Note, in the earlier step we already "installed" the inversify props into node_modules, now we're going to use that library.

* Create a new file in your `/src` directory called `app.container.ts`.  Inside that file you'll need to add just a few lines to start:

```js
import 'reflect-metadata'
// we will uncomment the next line out later once we have things to inject
// import { container } from 'inversify-props'

export default function buildDependencyContainer (): void {
  // once we have interfaces and implementations of services they will go in here
  // like:

  // container.bind<IBookService>(Registry.BookService1).to(BookService)

  // it seems overly verbose but here is basically what is happening:
  /*
    we are telling inversify that whenever an IBookService is requested
    to fullfil that with a BookService implementation

    The Registry.BookService1 provides a  unique key for this particular resolution
    that lets you have multiple implementations of an interface and return different
    resolutions based on the key used.

    So, if a component wanted to use this particular implmentation it would do this:

    @inject(Registry.BookService1)
    public bookService!: IBookService

    if there were a second implementation of IBookService it could be registered like so:

    container.bind<IBookService>(Registry.AlternateBookService).to(LibraryBookService)

    a component that wanted this implementation could then do the following:

    @inject(Registry.AlternateBookService)
    public bookService!: IBookService

    there is more to this process but it is beyond the scope of this post.
  */
}
```

That's it for now; becuase we don't have anything defined that we will actually inject yet we can't go any further with this file.  However, as we add injectable class definitions and interfaces we will be updating this file quite a bit.

Next, go to `/src/main.ts` and incorporate this file.  This is actually going to feel a little strange as we will be restructing a main part of the file.  This restructing will enable us to do quite a few other things as part of the bootstrapping of the Vue app - it sets up the dependency injection and we'll use it later when we incorporate vuex.

The current state of the project is [viewable at github](https://github.com/finalcut/vue-lootly/tree/2ea12e34cd2dd3b17db37ebfb9f1e9990a8b1fc9).

## Conclusion

I was going to get into the process of creating new components in this post but it's already pretty long.  We'll add a service, an interface, and a new component in the next post.  That should tie all this together in a tangible way.
