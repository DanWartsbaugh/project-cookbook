[X] log in - redirect to /mycookbook
[X] register - render form
[X] register - process form and redirect to dashboard
[X] log out
[x] dashboard - render dashboard.html (get_all_recipes(), goes to my cookbook)
[R] test kitchen - render (get_test_recipes(), which is like get_all but where test=true)
[X] search - render search.html
[X] new recipe - render new.html ('/mycookbook/new-recipe')
[ ] new recipe - process form and redirect to show page for that recipe
[R] show recipe - render show.html (recipe/<int:id>)
[ ] save recipe - add recipe to cookbook and redirect to show page for that recipe
[ ] send recipe to test kitchen - change test attribute to true and redirect to show in test page for that recipe
[R] edit recipe - render form (recipe/edit/<int:id>)
[ ] edit recipe - process form and redirect to show page for that recipe
[ ] delete recipe - redirect to dashboard
[ ] hide ingredients - on test page
[ ] show ingredients - on test page
[ ] new version - creates a new recipe (with an iterated version number) and redirects to edit page for that recipe
[ ] update version - do we need this one? could it be the same as edit?
[ ] delete version - delete recipe and redirect to test kitchen 
[ ] random recipe
[ ] filter recipes