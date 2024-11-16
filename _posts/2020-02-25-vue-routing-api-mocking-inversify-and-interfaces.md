---
layout: post
title: "Adding Interfaces and Models, a fake API, and Inversify!"
date: 2020-02-25
category: Programming
tags: [vue,typescript,vuetify,inversify,vue-router,json-server]
comments: true
featured: true
---
This is the third post in the [series](/2020/02/introducing-a-series-on-vue-js.html) using Vue 2.0

In [our last post](/2020/02/vue-material-design-and-dependency-injection.html) we laid a bunch of really useful groundwork but it probably didn't feel like we actually got anything done.  In this post we will be getting a few things completed and even showing some data on the page!  Yeah, that's right, we're going to show some productive work this time!

## Our First Model

The goal of this project is to track things you want to lend/borrow from your friends.  Historically, for me, I'm most likely to lend or borrow a book so we're going to start there.  Typescript supports interfaces so we'll define the basic structure of our book model as an interface.  In the `/src/` directory we'll create a `models` directory and, within there, we'll create our `IBook.ts` file.  **NOTE** some projects I've seen use a `types` folder instead of `models`.

```cs
/* IBook */
export default interface IBook {
  id: string // a uuid
  isbn: string
  title: string
  cover: string
  author: string
  genre: string
  thumbnail: string // to a url
  cover: string // to a url
  loanedTo: string
  loanedDate: Date
  isBorrowed(): boolean
}
```

I can already see I am going to have a few things that are shared across all borrowable item types.  `id, title, thumbnail, loanedTo, loandDate, isBorrowed()` so I'm going to create a second interface right now, `IBorrowable` that this interface will extend. I'm also going to rename `cover` to `primaryImageUrl` and `thumbnail` to `thumbnailUrl`.

```cs
/* IBorrowable */
export default interface IBorrowable {
  id: string // a uuid
  title: string
  thumbnailUrl: string // to a url
  primaryImageUrl: string // to a url
  loanedTo: string
  loanedDate: Date
  isBorrowed(): boolean
}

/* IBook */
import IBorrowable from './IBorrowable'

export default interface IBook extends IBorrowable {
  isbn: string
  author: string
  genre: string
  cover: string
}
```

## API Server - JSON Server

Now that we have a model we'll want a default implementation of a `Book` and a Service for getting instances of `Book` from the API.  API? We don't have an API yet.  That's a whole different project.  What we need now is a mock API. Basically, a fake webserver that let's us pretend like we're talking to the real deal.  Fortunately, the awesome project [JSON Server](https://github.com/typicode/json-server) exists just for this need.

This may be the easiest part of the entire project.  Install JSON Server.  We're installing it globally so it can be used on all sorts of projects.

```sh
npm install -g json-server
```

Now, what I do is I create a `server` directory beside my `src` directory and inside that folder I put a new empty file `api.json`.  Then I go into my `package.json` file and add the following line to the `scripts` section:

```js
    "api": "json-server --watch ./server/api.json --port 3001"
```

I am specifying the port becuase I use this on many projects.  Next, let's edit api.json and add the following

```js
{
  "books":[]
}
```

At this point you have defined an endpoint in your mock api called books.  WHen you call it you will get back an empty array of books.

Next, start the JSON Server so you can visit that endpoint:

```sh
npm run api
```

At this point you can hit the API in your browser at [http://localhost:3001/books](http://localhost:3001/books)  - If you don't have the `--port 3001` part of the command JSON server defaults to 3000

## Our First Service and Axios

In order for our project to make use of the API server we will need a service that is responsible for GET,POST (save), PUT (update), and DELETE (delete) of books.  Each of those four actions are called RESTful verbs.  Alternatively you could use PATCH for update.

Just like with our model above we will first define an Interface for our book service; `IBookService`.   We will first create a new folder in the `/src` directory called `services` and then create the file `IBookService.ts` in that directory.

```js
/* IBookService */

// the @ gets us back to the root of the project instead of having to use ../ for each directly level below the root you are at.
import IBook from '@/models/IBook'

export default interface IBookService{
  get(id: string): Promise<IBook>
  put(model: IBook): Promise<IBook>
  post(model: IBook): Promise<IBook>
  createItem() : IBook
}
```

Next we need an implementation of this service, so inside the `services` direcectory create an `impl` directory and, within that, create a file called `BookService.ts`.  We will start out with this structure:

```js
/* BookService */
import { injectable } from 'inversify-props'
import IBookService from '@/services/IBookService'
import IBook from '@/models/IBook'

// we need to use this attribute so we can use dependency injection via inversify later.
@injectable()
export default class BookService implements IBookService {
  get (id: string): Promise<IBook> {
    throw new Error('Method not implemented.')
  }

  put (model: IBook): Promise<IBook> {
    throw new Error('Method not implemented.')
  }

  post (model: IBook): Promise<IBook> {
    throw new Error('Method not implemented.')
  }

  createItem (): IBook {
    throw new Error('Method not implemented.')
  }
}
```

## Dependency Injection - Inversify

Since I've mentioned Inversify, let's register this service and it's interface with inversify so we can use it later.   First add a new file in the root of your project called `Registry.ts` and add the following:

```js
/* Registry.ts */
export interface IRegistry {
  [name: string]: symbol;
}

export const Registry: IRegistry = {
  IBookService: Symbol('BookService')
}
```

This basically creates a mapping of unique values that we will use to key our inversify registration with.  Next, go to `/src/app.container.ts` and update it to look like this:

```js
/* app.container.ts */
import 'reflect-metadata'
import { container } from 'inversify-props'
import { Registry } from './Registry'

import IBookService from './services/IBookService'
import BookService from './services/impl/BookService'

export default function buildDependencyContainer (): void {
  container.bind<IBookService>(Registry.IBookService).to(BookService)
}
```

Wow, we've actually done quite a bit already.  Let's make sure it all compiles and loads properly by entering `npm run serve` at the command line in the root of your project.  If all goes well you can launch the site at [http://localhost:8080](http://localhost:8080).  Sure, we didn't change what it's doing yet - but we know the dependency container loaded properly.

## Flush out the Service and the API a smidge

So right now our API doesn't do anything but return an empty array of books.  Let's add a single book.  Open `api.json` and change it to this:

```js
{
  "books":[
    {
      "id": "1",
      "title": "Milkman: A Novel",
      "thumbnailUrl": "",
      "primaryImageUrl": "https://images-na.ssl-images-amazon.com/images/I/41eOX0cBT8L._SX331_BO1,204,203,200_.jpg",
      "loanedTo": "",
      "loanedDate": "",
      "isbn": "1644450003",
      "author": "Anna Burns",
      "genre": "fiction",
      "cover": "paperback"
    }
  ]
}
```

Next we need to revisit our service and flush out the ability to get a book from the API.  To do that we will use Axios - a http library that lets us make RESTFUL api calls. Start by installing axios in your project

```sh
npm install axios
```

Open your BookService.ts file and include axios and then put it to use in the `get` method:

```js
import axios from 'axios'
...
  public async get (id: string): Promise<IBook> {
    const url = `http://localhost:3001/books/${id}`
    const httpResponse = await axios.get<IBook>(url)
    const model = httpResponse.data
    return model
  }
```

Honestly, having the url to the API hardcoded there is a really, really, bad idea.  Fortunatley, VUE gives us the ability to easily reference environment variables. To do that first create a file in the root of your project called `.env.development` and add the following lines:

```sh
VUE_APP_TITLE=Lootly (Dev)
VUE_APP_API_URL=http://localhost:3001
```

This defines two environment variables we will eventually make use of.  Right off the bat we'll use the API_URL one by going back to the `BookService` and updating it as follows:

```js
...
  protected readonly API_URL: string | undefined = process.env.VUE_APP_API_URL
  protected readonly END_POINT: string = 'books'

  public async get (id: string): Promise<IBook> {
    const url = `${this.API_URL}${this.END_POINT}/${id}`
    const httpResponse = await axios.get<IBook>(url)
    const model = httpResponse.data
    return model
  }
  ...
  ```

  We're actually setting ourselves up for some refactoring later where we can share the `get` method in various services - but we're not there yet.  We are at the point where we can use the service to get the book with id of `'1'` and then display it.  You can view the current state of the project at [GitHub](https://github.com/finalcut/vue-lootly/tree/339d7a92b925b181a0316c7039d51e1c6ad6cd8b).

## A Component

Honestly, we've done a lot to get to this point - but we're finally ready to tie everything together, grab a book and display it on the screen.

To start, create a new directory in the `/src/` directory called `components` and another directory under that called `book`.  In the `book` folder create a file called `Book.vue` which will be our *Single File Component (SFC)* for displaying the properties of a book.

The initial file will contain the following:

```js
/* Book.vue */

// all SFC start with a template.
// The template has to have one, and only one child
//  element (a <div> in this example.)
<template>
  <div v-if="model">
    <h1>{{model.title}}</h1>
  </div>
</template>

// we need to import a few things to make this all work.
<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator'
import { inject } from 'inversify-props'
import { Registry } from '@/Registry'
import IBook from '@/models/IBook'
import IBookService from '@/services/IBookService'

// in typescript we start with this attribute.
@Component({
  name: 'book'
})
// every component extends Vue at some point in a Vue app.
export default class extends Vue {
  // this is an argument than can be passed into the
  // component - it is the book we will be displaying info on
  @Prop(Object) readonly model!: IBook

  // we are going to use this service eventually, to update the book
  // mostly I'm just showing you how the dependency injection is called
  // within a component.
  @inject(Registry.IBookService)
  private bookService!: IBookService
};
</script>
```

Now we need to use the component.  For now, we're just going to use it right in the `App.vue`.

In `App.vue` we need to add the following code:

```js
...
import { inject } from 'inversify-props'
import { Registry } from './Registry'
import IBookService from './services/IBookService'
import Book from './components/book/Book.vue'
...
@Component({
  name: 'lootly',
  components: {
    book: Book
  }
})
...
  get AppTitle (): string { return 'lootly' }

  @inject(Registry.IBookService)
  private bookService!: IBookService
...
```

You can [see the full file on github](https://github.com/finalcut/vue-lootly/blob/a652935a728a54bdba3704a5702116897514d0b3/src/App.vue)

Finally, we need to use the bookservice to pull in the book and pass that book into the Book Component.

This will all happen in App.vue still.

1. Add a `created` method to the component which will use the Service to load the book.
2. add the `<book>` component into the template; passing along the book model from the service.

```js

  async created (): Promise<void> {
    this.bookService.get('1').then((result) => {
      this.book = result
    })
  }

```

and in the `template`:

```html

  <book :model="book" />

```

At this point you may get some things that don't work.  That is becuase we introduced some values in the `.env.development` file earlier.  But, becuase the server was already running via `npm run serve` those changes were never picked up.  We need to kill the app and then restart it. Find the terminal you started the app in and hit CTRL+C then reenter `npm run serve`

## Reflect.hasOwnMetadata is not a function

An error has arisen in the console in your browser.  This is a sneaky problem and I've made it happen on purpose.  If you look in `app.container.ts` we are `import 'reflect-metadata'` which seems like it should fix this problem.

However, the order you import it in is very important.  If you want to use this `reflect-metadata` library it needs to be the imported before you do any kinds of `@injects` - but in our App.vue file we are now injecting the `IBookService`.

If you go to the `main.ts` file you will see the files are imported in the following order:

```js
import { Vue } from 'vue-property-decorator'
import App from '@/App.vue'
import vuetify from '@/plugins/vuetify'
import buildDependencyContainer from '@/app.container'
```

`App` comes before `app.container` so the `reflect-metadata` is being loaded too late!  To solve this just remove the `import reflect-metadata` from `app.container.ts` and put it at the top of `main.ts`.

## Nothing is appearing on the page

The VSCode editor is pretty good at fixing bad html.  However, if you aren't paying attention you could end up putting some html where you don't want it.

For instance, if you put your `<book>` component in the `App.vue` template incorrectly you may not see anything.  Here is how it would be if it were incorrect:

```html
    <v-content>
      <v-container
        class="fill-height"
        fluid
      />
      <book :model="book" />
    </v-content>
```

Note, `v-container` is a self-closing tag.  SO the `<book>` tag you in won't appear at all.

Instead change that snippet to:

```html
    <v-content>
      <v-container
        class="fill-height"
        fluid
      >
        <book :model="book" />
      </v-container>
    </v-content>
```

And you'll be good to go.  It won't look great on the page but it will show you  **Milkman: A Novel** in big, bold text.  It's a start!

## Environment Variables Revisited

WHile we are in `App.vue` let's remove the string `lootly` from  78 and use our enviornment variable of VUE_APP_TITLE:

```js
  get AppTitle (): string { return process.env.VUE_APP_TITLE }
```

Now the header will say **Lootly (Dev)**

## Conclusion

In this phase we tied a lot of things together.  We've added a service, an implementation of the service, a model interface, a mock api that implements the model interface, a component that displays the model, and we've used that component as a new `html` tag of `book`!

Overall, that's a pretty good day.  In the next article we'll look at making some of our code more reusable with the help of generics and inheiritance.

You can see [the state of the projects code, at this point, on github](https://github.com/finalcut/vue-lootly/commit/898bfaf770ecfa32a7a369a7c39da0370bb8dc51)
