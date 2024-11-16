---
layout: post
title: "Unit Testing Coldfusion (CFC) Private Methods"
date: 2009-01-06
comments: false
categories:
 - coldfusion
 - cfc
 - unit testing
 - mxunit
---
To be honest I've not really seen much written detailing good (or even
standard) ways of unit testing private methods without making their scope less
restrictive than private. Thus I'll detail the way a co-worker a technique a
co-worker and I came up with that seems like it will work pretty well. If you
see any potential problems with this approach please just let me know in the
comments.  
  
The approach is fairly simple. We create a helper class that extends and
"wraps" our class to be tested. This helper class then has simple methods in
it that expose the private methods via a wrapper. So let's say we had a class,
MoneyLender, with the private method of computeInterest(). Let's ignore
whether that method should be private or not for arguments sake. We would
create a MoneyLenderTestHelper class with a method in it called
computerInterestWrapper() which actually just returns the private
computeInterest method.  
  
Right off the bat I have one potential concern and that is will the other
private things (methods, member variables, etc) still be exposed to the
private method that is being returned? I haven't tested this out yet so I
don't know.  
  
Anyway, my test would then instantiate the MoneyLenderTestHelper class, and
call the computeInterestWrapper() method to get a reference to the private
method to be tested. Then I could execute the method and perform the test. If
the test needed to analyze the state of any private member variables I could
create a helper method in MoneyLenderTestHelper that would inspect the private
variable.  
  
The main reason for returning a reference to the method in the helper class,
instead of calling the helper method there, was so that I don't have to
maintain the method signature in both the class being tested and in the helper
class. My test obviously has to know the signature but overall this seems more
maintainable.  
  
What do you think? I'll post more as I muck around with the approach and let
you know how well it all works. We've already implemented the idea on a few
test cases but the private methods don't actually touch any private member
variables; however, in the cases we have tried it with the technique has
worked out well.

## Comments

Marc Esher

the "makePublic" stuff in mxunit basically just does some dynamic cfc
generation and some method-name swapping. it ain't purty, but then most
class/method monkeying isn't.  
  
when I added it to mxunit, I added it for pretty much exactly the reasons Bill
described in his last comment. I use testing to help me code better and
faster, bottom line. And when I'm writing private functions, sometimes they
make themselves test-worthy. Sometimes that's an immediate code smell to me
and I catch myself. But sometimes, it's legitimate. Sometimes the private
function is doing something complicated that I just can't get my mind around
and I need to see what's going on, and it's easiest for me to whip up a test
and execute that private method directly. Often, I will take out the private
method tests from my test cases because they've served their purpose, which
is: to help me run my code in isolation so that I can achieve the behavior I
want to achieve and move on to the next thing.  
  
In my own experience, I haven't seen that the existence of makePublic leads me
to a bias towards testing private methods. I have found that I'm glad it's
there when I need it.  
  
thanks for the post Bill!

Bill

Tom,  
I don't create unit tests for all of my private methods but occasionally one
pops up that needs specific fine grain testing.  
  
The private methods are a foundation upon which my public methods are built
upon, if the private method ends up with a bug then my public method will
fail; sometimes it is more efficient to make sure the private method works
exactly as expected (via unit testing).  
  
I could just write a unit test against the public methods that call the
private methods but that is neither efficient (in regards to testing time) nor
is it always clear what functionality exactly is being tested.  
  
In the end I suppose it might be a personal preference; but some methods are
critical enough that I think they warrant their own set of unit tests even if
the method is private. Likewise, if an error is discovered through usage of
the system and, via, debugging, I find out the error is specifically related
to a private method I like to write my unit test to duplicate the problem such
that I am testing the failing private method directly with data that I know
caused the problem. This way if the public method has logic that transforms
the data I don't have to worry about that transformation logic changing and
thus invalidating my very specific unit test.

Tom Chiverton

Why would you want to unit test private methods ? Those are almost by
definition part of the internal workings of the class, whereas you should just
be making sure the exposed interface is correct, no ?

Rich

You can read more at http://mxunit.org/doc/index.cfm?doc=testprivate, but
basically it seems like the original method is renamed (at least for the
instance of the object at runtime for your unit test), and a new public method
with the same name and functionality is injected.

Bill

well that's an interesting and handy feature. What does it do, make a copy of
the function and use method injection?

Rich

If you are using MXUnit, you can just call the makePublic() method, and then
test your private method like it were public.

