---
layout: post
title: "Unit Testing - KISS and DRY"
date: 2007-02-12
category: c#
tags: [unittesting,nunit,kiss,dry,patterns,objectmother]
---
Everyone knows unit testing is a good idea - but, let's face it, some times it
can be a real pain in the but. Writing all that tedious setup code, over and
over and over can drive anyone crazy and, perhaps, cause some people to stop
writing unit tests.

Well, there is a painfully obvious solution to this problem - it's called the
[Object Mother Pattern](http://www.agilealliance.org/show/910). The folks who
wrote the linked to pdf explain the pattern well enough that I don't think I
should rehash it here. However, don't let my lack of description stop you from
checking it out. It could very well save you a ton of repetitious typing.

Here is an example of a unit test "setup" procedure that could be so much
cleaner (and simpler) had I used the ObjectMother pattern when I wrote this
test:

```c#
private Client m_client = new Client();
private Agency m_agency = new Agency();
private PPCR m_ppcr = new PPCR();
private Patient m_patient = new Patient();
private MedicationsAdministered m_medsadministered = new
MedicationsAdministered();
private MedicationsAdministeredProperty m_medsadminprop = new
MedicationsAdministeredProperty();
private Element m_element = new Element();
private ElementValue m_elementvalue = new ElementValue();

...
[SetUp]
public void SetUp()
{
  m_agency.AddNew();
  m_agency.AgencyID = agencyid;
  m_agency.AddedBy = adminUserID;
  m_agency.AddedDate = new DateTime(2000, 1, 1);
  m_agency.UpdatedDate = new DateTime(2000, 1, 1);
  m_agency.AgencyNumber = "1";
  m_agency.AgencyName = "TEST";
  m_agency.AgencyState = "WV";
  m_agency.ContractExpiration = new DateTime(2099, 1, 1);
  m_agency.UpdatedBy = adminUserID;
  m_agency.DeletedInd = false;
  m_agency.Save();

  m_client.AddNew();
  m_client.AgencyID = m_agency.AgencyID;
  m_client.ClientID = clientid;
  m_client.Title = "Tester";
  m_client.Description = "I represent a tester";
  m_client.LastConnectDate = DateTime.Now;
  m_client.AddedDate = DateTime.Now;
  m_client.UpdatedBy = adminUserID;
  m_client.UpdatedDate = DateTime.Now;
  m_client.DeletedInd = false;
  m_client.Save();

  m_ppcr.AddNew();
  m_ppcr.AgencyID = m_agency.AgencyID;
  m_ppcr.PPCRID = ppcrid;
  m_ppcr.AddedBy = adminUserID;
  m_ppcr.AddedDate = DateTime.Now;
  m_ppcr.DeletedInd = false;
  m_ppcr.UpdatedBy = adminUserID;
  m_ppcr.UpdatedDate = DateTime.Now;
  m_ppcr.PPCRNumber = "1";
  m_ppcr.Save();

  m_patient.AddNew();
  m_patient.PPCRID = m_ppcr.PPCRID;
  m_patient.PatientID = patientid;
  m_patient.PatientNumber = 0;
  m_patient.AddedBy = adminUserID;
  m_patient.AddedDate = DateTime.Now;
  m_patient.DeletedInd = false;
  m_patient.UpdatedBy = adminUserID;
  m_patient.UpdatedDate = DateTime.Now;
  m_patient.Save();

  m_element.AddNew();
  m_element.ElementID = elementid;
  m_element.ElementName = "TESTELEMENT";
  m_element.ElementEnum = Element.Elements.WorkRelated.ToString();
  m_element.AttributeType = "TEST";
  m_element.ElementCode = "TEST";
  m_element.AddedBy = adminUserID;
  m_element.AddedDate = new DateTime(2000, 1, 1);
  m_element.UpdatedDate = new DateTime(2000, 1, 1);
  m_element.UpdatedBy = adminUserID;
  m_element.DeletedInd = false;
  m_element.Save();

  m_elementvalue.AddNew();
  m_elementvalue.ElementValueID = elementvalueid;
  m_elementvalue.AgencyID = m_agency.AgencyID;
  m_elementvalue.ElementID = m_element.ElementID;
  m_elementvalue.AddedBy = adminUserID;
  m_elementvalue.AddedDate = DateTime.Now;
  m_elementvalue.UpdatedBy = adminUserID;
  m_elementvalue.UpdatedDate = new DateTime(2000, 1, 1);
  m_elementvalue.DeletedInd = false;
  m_elementvalue.Value = "TESTELEMENT";
  m_elementvalue.SortOrder = 0;
  m_elementvalue.Save();


  m_medsadministered.AddNew();
  m_medsadministered.MedicationsAdministeredID = medsadminid;
  m_medsadministered.PPCRID = m_ppcr.PPCRID;
  m_medsadministered.PatientID = m_patient.PatientID;
  m_medsadministered.AddedBy = adminUserID;
  m_medsadministered.AddedDate = new DateTime(2000, 1, 1);
  m_medsadministered.UpdatedDate = new DateTime(2000, 1, 1);
  m_medsadministered.UpdatedBy = adminUserID;
  m_medsadministered.DeletedInd = false;
  m_medsadministered.Save();

  m_medsadminprop.AddNew();
  m_medsadminprop.MedicationsAdministeredPropertyID = medsadminpropid;
  m_medsadminprop.MedicationsAdministeredID =
  m_medsadministered.MedicationsAdministeredID;
  m_medsadminprop.ElementID = m_element.ElementID;
  m_medsadminprop.ElementValueID = m_elementvalue.ElementValueID;
  m_medsadminprop.AddedDate = new DateTime(2000, 1, 1);
  m_medsadminprop.UpdatedDate = new DateTime(2000, 1, 1);
  m_medsadminprop.DeletedInd = false;
  m_medsadminprop.Save();

}

```


All of that had to be created and dealt with just so I could test the methods
on the MedicationsAdministeredProperty object. However, had I used the
ObjectMother pattern I would have just written

```c#
private MedicationsAdministeredProperty m_medsadminprop = ObjectMother.createNewMedicationAdministeredProperty();

```


Considering a lot of that code (pre ObjectMother) was used to test the
MedicationsAdministered Object, the Patient, the PPCR, the Agency, the Client,
etc. (just smaller subsets) it should be clear how obvious this pattern is,
and thus, how helpful it is.

So go on, go read that PDF - a few minutes spent now will save you a ton of
time later.
