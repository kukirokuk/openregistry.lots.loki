.. _tutorial:

Tutorial
========

Exploring basic rules
---------------------

Let's try exploring the `/lots` endpoint:

**************************************

Just invoking it reveals empty set.

Now let's attempt creating a lot:

*******************************************

Error states that the only accepted Content-Type is `application/json`.

Let's satisfy the Content-type requirement:

*********************************

Error states that no `data` has been found in JSON body.


.. index:: Lot

Creating lot
------------

Let's create lot with the minimal data set:

**************************************

The object you're trying to add initially receives `draft` status. You should manually switch this object from `draft` to `composing` (2 Phase Commit mechanism) so that to add the auction conditions (value.amount, minimalStep.amount, etc.):

**************************************

You see that `lot.auctions` structure has been added with the set of auto-generated data. 

Now let's add extra auction conditions. Note that the information is being added to each of three auctions one by one:

************************************** 

**************************************

**************************************

To enable further manipulations with the lot, its status should be manually switched to `verification`.

**************************************

Success! Now we can see that new object was created. Response code is `201`
and `Location` response header reports the location of the created object.  The
body of response reveals the information about the created asset: its internal
`id` (that matches the `Location` segment), its official `assetID` and
`dateModified` datestamp stating the moment when asset was last
modified. Note that lot is created with `pending` status.

Let's access the URL of the created object (the `Location` header of the response):

**************************************

.. XXX body is empty for some reason (printf fails)

We can see the same response we got after creating lot.

**************************************

Let's see what listing of lots reveals us:

**************************************

We do see the internal `id` of the lot (that can be used to construct full URL `**************************************`) and its `dateModified` date stamp.

Let's try creating another lot:

**************************************

**************************************

.. XXX patching lot to pending.dissolution

**************************************

And again we have `201 Created` response code, `Location` header and body with extra `id`, `lotID`, and `dateModified` properties.

Let's check what lot registry contains:

**************************************

And indeed we have 2 lots now.


Modifying Lot
-------------

Let's update lot description:

**************************************

.. XXX body is empty for some reason (printf fails)

We see the added properties have merged with existing lot data. Additionally, the `dateModified` property was updated to reflect the last modification date stamp.

`Note` that lot can be modified only within the rectification period (up to `rectificationPeriod.endDate`).

Checking the listing again reflects the new modification date:

**************************************

Deleting Lot
------------

Let's delete lot:

A document with the `documentType: canellationDetails` has to be added first:

**************************************

So now lot can be easily deleted:

**************************************

Integration with assets


Concierge operations
--------------------

For lot to be formed, you need to specify id of the asset which is to be included 
in that lot. If this assets is available, it will be attached to lot 
and status of a lot itself will be changed to `pending`:

**************************************

In case of this assets is unavailable, status of the current lot will turn to `invalid`:

**************************************

When bot finds that status of lot is `pending.deleted`, it
turns status of the asset being attached to that lot to `pending`. Status of the lot itself will become `deleted`.
   
**************************************

When bot finds that status of lot is `pending.dissolution`, it
turns status of the asset being attached to that lot to `pending`. Status of the lot itself will become `dissolved`.
   
**************************************

When bot finds that status of lot is `pending.sold`, it
turns status of the asset being attached to that lot to `complete`. Status of the lot itself
turns to `sold`.

**************************************
   
Convoy operations
-----------------

The procedure will be formed automatically after `rectificationPeriod.endDate`. For this to be done, lot status automatically receives `active.salable` at first.

**************************************

**************************************

When the procedure is successfully created, lot status changes to 
`active.auction`: 

**************************************

If the procedure (`procurementMethodType: sellout.english`) becomes `unsuccessful`, lot status turns to `active.salable`.

**************************************

As long as a new procedure is being automatically created, the lot will be given `active.auction` status:

**************************************

In case of that lot has not been sold (either `contract` has become `unsuccessful` or a procedure has received `cancelled` status or third procedure (`procurementMethodType: sellout.insider`) has turned to `unsuccessful`) , its status becomes `pending.dissolution`:

**************************************

When contract has been successfully created within the Module of Contracting, lot's status turns to `active.contracting`:

**************************************

When contract reaches `terminated` status, lot automatically becomes `pending.sold`:

**************************************
