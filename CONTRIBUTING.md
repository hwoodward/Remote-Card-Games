<h3>Thank you for wanting to contribute, however before you do there are some things you should know.</h3>

<h4>Have a plan</h4>

* When working on an issue or feature that is already planned read up on what the plan is and follow it. 
  * If you find a problem with the plan let whoever wrote it know and work with them to make a new design plan.
* When starting on an issue without a clear design, make one and write it down in the issue before you implement it

<h4>Test your code</h4>

* We expect you to have tested your code contributions for functionality
* We expect you to add unit tests where appropriate (see unit testing segment below for details but more unit tests are better).
  * If you are not familiar with unit testing in python figure out what you need to test and ask for help.

<h4>Document your work</h4>

* Document what you implemented and how it works. If you aren't sure how write your decisions down somewhere and ask your reviewer for help.
  * See the documentation section for where to find information you may need and where to put information on your work.
* If you aren't comfortable with some or all of our documentation methods:

<h4>Link to issues</h4>

* If your code is associated with an issue you are solving, please link it in the pull request so we can close it.

<h4>Find a reviewer</h4>

* When you create a pull request please assign it to someone for review - this will get your code merged quicker.
  * If you aren't sure who to assign it to Helen is an acceptable default choice.

<hr>

<h3>Documentation: the wiki, issues, and other</h3>
We put information in a lot of places for this project, but it generally breaks down into 3 categories:
1. Information about how to run the program goes in the README
2. Information relevant to understanding the code goes in the WIKI
    1. This includes overall design, the API specifications, and more detailed design docs about the components
3. The rules of the card games and how to play them (both what buttons do what and what options are legal) go in teh WIKI
    1. Eventually there should be help information available in the app itself, but its not a priority and the rules are more relevant to writing code to enforce them then to actually starting the program.
4. Unfinalized information goes in the relevant issue, see the segment on work tracking for details

If you are unsure the wiki is a good default, things can always be moved later.

When trying to find out somehting about this project I recommend the following order of search:
1. See if there is an open issue already
    1. If so read that discussion, referencing the wiki as needed for background info
2. Check the wiki/README/etc. for relevant information.
    1. Pick what to check first based on the categories above.
    2. The docs available outside the wiki include the README, this contribution guide, and the style guide (once we have one, its currently a TODO)
3. Finally check if there is a card for it in any projects.
    1. Since cards are likely very vague when you do find one feel free to convert it to an issue and comment there asking for information
4. If you haven't found the information you were looking for you can message someone in the project and if it is a signficant topic you can't figure out, open an issue (I recommend labelling it question and/or enhancement)

<hr>

<h3>Unit Testing</h3>
We want things to be unit tested. If you add a new class, unit test it when at all possible.

Things we require be unit tested:
* Common classes
  * Classes in the common package are meant to be pretty dang modular and should never be impossible to unit test.
* State trackers
  * state classes inherently don't communicate and so should be unit tested. 
  * Basically anything that can be set in the state needs to be tested that it is stored properly and amended properly when appropriate.
  * state trackers can use a SUPER simple standin ruleset to test rule verification. the goal in testing the state tracker is to confirm it CALLED the rules not to check the rules implement the game properly. The rules are unit tested on their own for properly matching the actual game

Things we intentionally don't unit test:
* Network send/recieve methods
  * This would just add ANOTHER place to keep in sync if we change an API
  * These methods should be super simple and consiste solely of constructing/deconstructing the json and calling a helper
  * Also podsixnet has standalone tests that communications reach their destination properly
* The UI as of right now
  * We don't have one yet but UI render testing is hard to unit test b/c it involves confirming a render looks correct.
  * We expect you to test that any UI changes still work manually - and a test class may be added to let you do so more easily in the future.

<hr>

<h3>Work Tracking</h3>

To make life easier as work on this project is sporadic we utilize githubs issue tracking and projects to keep track of what the priority to work on is and what state various ongoing work is in.

* Projects organize bits of work that need to be done to achieve a goal.
  * Some, like documentation, are ongoing, and as new tasks related to them come up they are added
  * Others are finite and mark significant functionality progress on the game. For those most of the tasks are added at creation and it is only edited to split them into more manageable pieces as necessary.
* Issues are specific topics that need to be addressed, and almost always map to a task that goes in a project
  * Issues fall into a few categories, such as bugs, features (or enhancements which may become features), or possibly questions and are closed when there is no longer work relevant to them to do.

How work flows through the system:
1. A task is created either as a card in a project or as an opened issue
    1. If a card is made then it needs to be translated to an issue. Feel free to translate cards to issues and link them when you have time. Especially if you understand the task being described or want to do it.
2. The issue is tagged, assigned, and commented on
    1. When you create an issue PLEASE tag it as accurately as you can, and if you know who needs to be involved with it assign the issue or mention them.
        1. If an issue represents a task that belongs in a project please link a card in that project. (create one if you need to, but check before making duplicates)
    2. Feel free to edit the tags on issues as the project status changes
    3. Feel free to assign unassigned issues to yourself if you are going to work on them
    4. If you have ideas on the design of a feature or enhancement please join the discussion in that issues comments.
3. Code writing begins if relevant
    1. All work should be done in a sanely named branch.
    2. When you start this step make sure the issue is assigned to you and the card in the project is moved to 'in progress'
    3. When you are finished with your code remember to:
        1. Test your work
        2. Link the issue in your pull request (this should move your card to 'Needs Review' column)
        3. Assign a reviewer
4. The issue is closed and the card moves to Done
    1. For questions this may not involve any work outside of the issue
    2. For bugs that are determined not to impeded use of the game this CAN be after tagging 'won't fix'
    3. For all other issues this requires some amount of documentation.
        1. For enhancemnents that are out of scope, note that it was out of scope in the relevant segments wiki page
        2. For features that are finished make sure that the design was documented in the wiki
        3. For bug fixes make sure any design changes are documented (this may not be relevant for small changes)
