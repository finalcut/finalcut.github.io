---
layout: post
title: "Enable/Disable an Enrollment in Blackboard Learn using IMS XML"
date: 2012-01-27
comments: false
---
Honestly, this seemed like it would be a straight forward process.  Blackboard
certainly hints at it being simple and straightforward.  But it turns out
disabling (and re-enabling) an enrollment isn't as obvious as you might hope.

XML

There is a bit of conflicting documentation but this is how we ended up
getting it to work using Blackboard Learn 9.1 SP 8.



  1. login to blackboard learn
  2. go to the system admin tab
  3. go to data integration
  4. select student information system integrations
  5. select your xml integration option (I'm not going into how to create one)
  6. in the little arrow drop down pick "Edit"
  7. make sure on the Enrollments row that "deletes" is set to "Disable"
  8. go back to the Student information system integrations page
  9. using the arrow drop down pick "Advanced Configuration"
  10. use the arrow drop down on enrollment and pick "Field Mapping"
  11. CHECK the "change or update?" box for "Row Status"
  12. Tell it to use a "Custom Script" and paste in this script:

```js
var rs = true;
if ( data.rolesToAddOrUpdate.get(0).status = 0 ) {
rs = false;
}
rs;

```


**WARNING**:  If you don't setup blackboard as indicated then including recstatus=3 as an attribute on the ROLE node will cause the enrollment to be DELETED from blackboard.  This will cause all artifacts created by that user within that class to be disassociated from them; thus if they are re-enrolled in the class they won't be tied to any of those artifacts.  Many of the artifacts will still be there; they'll just be associated with Anonymous.



By disabling the enrollment the artifacts remain associated with the user so
that when they are reenrolled in the class they don't have to re-upload all of
their assignments etc.



This process is useful for dealing with drops/holds on students as well so
that their enrollment in the class isn't deleted (though it does disappear
from the students interface) until their enrollment is reinstated.




Flat Files

If you are using the flat file (pipe delimited) process between banner and
blackboard things are more straightforward.  You just have to include the
column "ROW_STATUS" with a value of "disabled" in order to disable an
enrollment and "enabled" to enable the enrollment.



A disabled enrollment using either of these methods will appear in to an
administrator (and perhaps in some other scenarios) with a small red circle to
the left of the enrollment record.

You can learn about more of the process and the difficulties that were
experienced in our transition from Vista to Learn over at [John Cummings
blog](http://www.jcummings.net/ims-enterprise-1-1-vista-xml-integration-
blackboard-learn-9-and-processing-enrollment-changes/)

