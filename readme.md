# 1. Create a new object

```python
from core.models import Simple
obj = Simple(text='Text from shell', number=3, url='www.google.com')
obj.save()
print(obj) # <Simple: Text from shell>
```

# 2. Update an object

```python
get_obj = Simple.objects.get(id=1)
get_obj.number = 10
get_obj.save()
```

# 3. Delete an object

```python
del_obj = Simple.objects.get(id=1)
del_obj.delete()
```


# 4. Get one record

```python
from core.models import Simple
obj_1 = Simple(text='Object 1', number=3, url='www.google.com')
obj_1.save()
obj_2 = Simple(text='Object 2', number=3, url='www.yahoo.com')
obj_2.save()
# .get() works only with unique columns like id
get_obj_1 = Simple.objects.get(id=3)
# .filter() works for columns with non unique columns which returns a QuerySet [i.e collection of objects]
get_objects = Simple.objects.filter(number=3)
```

# 5. Get multiple records

```python
from core.models import Simple
all_objects = Simple.objects.all()

for r in all_objects:
    print(f'{r.text} has {r.number} numbers')

first_record = all_objects[0]
first_record.number = 20
first_record.save()
```

# 6. Get filtered records

```python
from core.models import Simple
get_objects = Simple.objects.filter(number=10)
```

# 7. Get excluded records

```python
from core.models import Simple
# .exclude() is the opposite of filter. It will return all the object except the ones having number=10
get_objects = Simple.objects.exclude(number=10)
```

# 8. Chaining Filters

```python
from core.models import Simple
Simple.objects.filter(number=10).filter(url='http://www.yahoo.com') # will return a QuerySet

# or

results = Simple.objects.filter(number=10)
results.filter(url='http://www.yahoo.com') # Will return a QuerySet
```

# 9. Field Lookups

```python
Simple.objects.get(id__exact=14)
# SELECT ... WHERE id = 14;

Simple.objects.get(id__exact=None)
# SELECT ... WHERE id IS NULL;

Simple.objects.get(title__iexact='beatles blog')
# SELECT ... WHERE title ILIKE 'beatles blog';

Simple.objects.get(title__iexact=None)
# SELECT ... WHERE title IS NULL;

Simple.objects.get(title__contains='Lemon')
# SELECT ... WHERE title LIKE '%Lennon%';

Simple.objects.get(title__icontains='Lemon')
# SELECT ... WHERE title ILIKE '%Lennon%';

Simple.objects.filter(id__in=[1, 3, 4])
# SELECT ... WHERE id IN (1, 3, 4);

Simple.objects.filter(title__in='abc')
# SELECT ... WHERE headline IN ('a', 'b', 'c');

# NOTE: You can also use a queryset to dynamically evaluate the list of values instead of providing a list of literal values:

inner_qs = Blog.objects.filter(name__contains='Cheddar')
entries = Entry.objects.fitler(blog__in=inner_qs)

SELECT ... WHERE blog.id IN (SELECT id FROM ... WHERE NAME LIKE '%Cheddar%')


# MORE : https://docs.djangoproject.com/en/3.1/ref/models/querysets/#id4
```

# 10. Limits and Offsets

```python
Simple.objects.all()[:5] # Limit to first 5 records
Simple.objects.all()[1:] # Offset one, means it will skip first record and get the remaining
Simple.objects.all()[5:] # Offset one, means it will skip first five record and get the remaining
Simple.objects.all()[:] # Offset none, means it will get all the records
Simple.objects.all()[1:3] # Offset none, Limit to 3 means it skips first records and return the next 2 records (3-2)
```

# 11. Order BY

```python
Simple.objects.all() # Returns records as got from database
Simple.objects.order_by('id') # ORDER BY id ASC
Simple.objects.order_by('-id') # ORDER BY id DESC
Simple.objects.order_by('url') # ORDER BY url ASC
Simple.objects.order_by('-url') # ORDER BY url DESC
Simple.objects.order_by('number', '-url')
Simple.objects.order_by('number', '-url')[:3]
```

# 12. Get Count

```python
Simple.objects.count()
Simple.objects.filter(number=10).count()
```

# 13. Using Dates

```python
from datetime import datetime

# Store datetime in database
new_date = datetime.now()
my_date = DateExample(the_date=new_date)
my_date.save()

# Query using datetime
DateExample.objects.filter(the_date__date=new_date) # Queryset
DateExample.objects.filter(the_date__time=new_date) # Queryset
DateExample.objects.filter(the_date__momth=3) # Queryset
DateExample.objects.filter(the_date__day=14) # Queryset
```

# 14. Is Null

```python
Simple.objects.filter(url__isnull=True) # Queryset
Simple.objects.filter(url__isnull=False) # Queryset
```

# 15. Many TO Many Relationship

```python
class Language(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name


class Framework(models.Model):
	name = models.CharField(max_length=100)
	language = models.ForeignKey(Language, on_delete=models.CASCADE)

	def __str__(self):
		return self.name

# Insert To Parent Model
from core.models import Language, Framework
python = Language(name='Python')
python.save()

# Insert To Child Model
django = Framework(name='Django')
django.language=python
django.save()

# Insert To Child Model
flask = Framework(name='Flask')
flask.language=flask
flask.save()

# Insert To Child Model
bottle = Framework(name='Bottle', language=python)
bottle.save()

# Get Child Model by Filtering with Child Model.name
# <Child>.objects.filter(<parent>__name='Python')
Framework.objects.filter(language__name='Python')

# Get Child Model by Filtering with Child Model.name and Field Lookup
# <Child>.objects.filter(<parent>__name__startswith='Py')
Framework.objects.filter(language__name__startswith='Py')

# Get Parent Model by Filtering with Parent model.name
# <Child>.objects.filter(<parent>__name='Flask')
Language.objects.filter(framework__name='Flask')
```

# 16. Many To Many Relationships

```python
class Movie(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name


class Character(models.Model):
	name = models.CharField(max_length=100)
    # ManyToManyField can be placed in any ome of the Model but better to place it on a Lower Level Model.
    # Here Movie Model holds a higher Level than Character
	movies = models.ManyToManyField(Movie, related_name='characters')

	def __str__(self):
		return self.name


# Create Movies
avengers = Movie(name='Avengers')
avengers.save()

# Create Character
thor_character = Character(name='Thor')
thor_character.save()

# Add Movie to a Character
thor_character.movies.add(thor)
thor_character.movies.add(avengers)

# Instead of creating a movie and adding separately, we can create a movie for a character directly
captain_america.movies.create(name='Winter Soldier')

# Reverse Relationship as below

# Create Movie
batman = Movie(name="Batman")
batman.save()

# Create Character
robin = Character(name="Robin")
robin.save()

# Add Character to a Movie
batman.characters.add(robin)

# Instead of creating a character and adding separately, we can create a character for a movie directly
batman.characters.create(name="Cat Woman")
```

# 16. Many To Many Relationships Queries

```python
# Get all Characters by movie name (One Step)
Character.objects.filter(movies__name='Batman') # QuerySet

# Get all Characters by movie name (Two Step)
avengers = Movie.objects.get(name='Avenger')
avenger.characters.all() # QuerySet

# Get all Movies of a Character (One Step)
Movie.objects.filter(characters__name='Batwoman') # QuerySet

# Get all Movies of a Character (Two Step)
batwoman = Character.objects.get(name='Batwoman')
batwoman.movies.all() # QuerySet
```

# 17. Attach multiple Objects using Many To Many Relationships

```python
bar1 = Bar.objects.get(pk=1)
bar2 = Bar.objects.get(pk=2)

foo = Foo()
foo.save()

# Slow - 7 Queries
foo.bars.add(bar1)
foo.bars.add(bar2

# Slow - 6 Queries
foo.bars.add(bar1, bar2)

# Slow - 5 Queries
foo.bars = [1,2]

# Fast - 4 Queries
foo.bars.add(1,2)
```