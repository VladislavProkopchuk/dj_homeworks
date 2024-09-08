import pytest
from rest_framework.reverse import reverse
from model_bakery import baker
from rest_framework.test import APIClient
from rest_framework import status

from students.models import Course, Student


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def course_factory():
    def factory(count_students=5, *args, **kwargs):
        students_set = baker.prepare(Student, _quantity=count_students)
        course = baker.make(Course, students=students_set, *args, **kwargs)
        return course

    return factory


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        student = baker.make(Student, *args, **kwargs)
        return student

    return factory


@pytest.fixture
def courses(course_factory):
    n_courses = 10
    return course_factory(_quantity=n_courses)


@pytest.mark.django_db
def test_get_course(client, courses):
    """ проверка получения 1го курса """
    id = courses[0].id
    response = client.get(reverse('courses-detail', args=[id]))
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data['id'] == id
    assert data['name'] == courses[id - 1].name


@pytest.mark.django_db
def test_get_courses_list(client, courses):
    """ проверка получения списка курсов """
    response = client.get(reverse('courses-list'))
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == len(courses)
    assert data[-1]['name'] == courses[-1].name


@pytest.mark.django_db
def test_filter_courses_by_id(client, courses):
    """ проверка фильтрации списка курсов по id """
    courses_expected = [courses[0], courses[-1]]
    ids = [course.id for course in courses_expected]
    # url = reverse('courses-list') + '?' + '&'.join('id=' + str(id) for id in ids)
    response = client.get(reverse('courses-list'), data={"id": ids})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == len(ids)
    for i, id in enumerate(ids):
        # id-1 , т.к. нумерация листа courses начинается с нуля, а запись в БД с 1
        assert data[i]['id'] == courses_expected[i].id
        assert data[i]['name'] == courses_expected[i].name


@pytest.mark.django_db
def test_filter_courses_by_name(client, courses):
    """ проверка фильтрации списка курсов по name """
    test_id = 3
    name_course = courses[test_id - 1].name
    # url = '/api/v1/courses/?'+'&'.join('name=' + name for name in names_course)
    response = client.get(reverse('courses-list'), {'name': name_course})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    # id-1 , т.к. нумерация листа courses начинается с нуля, а запись в БД с 1
    assert data[0]['id'] == courses[test_id - 1].id
    assert data[0]['name'] == courses[test_id - 1].name


@pytest.mark.django_db
def test_post_course(client):
    """ тест успешного создания курса """
    name_test = 'fred123asdasd'
    course = Course.objects.filter(name=name_test)
    assert len(course) == 0
    count_courses = Course.objects.count()

    response = client.post(reverse('courses-list'), {'name': name_test})
    assert response.status_code == status.HTTP_201_CREATED, response.content

    # проверяем что записали
    assert Course.objects.count() == count_courses + 1
    course = Course.objects.filter(name=name_test)
    assert len(course) == 1


@pytest.mark.django_db
def test_update_course(client, courses):
    """ тест успешного обновления курса """
    name_test = 'fred123asdasd'

    # проверяем, что тестовое имя отсутствует в БД
    course = Course.objects.filter(name=name_test)
    assert len(course) == 0

    # теперь обновим один из курсов
    id = courses[0].id
    response = client.patch(
        reverse('courses-detail', args=[id]),
        data={'name': name_test}
    )
    assert response.status_code == status.HTTP_200_OK, response.content

    # и проверим, что курс обновился
    course = Course.objects.filter(name=name_test)
    assert len(course) == 1


# тест успешного удаления курса
@pytest.mark.django_db
def test_del_course(client):
    name_test = 'fred123asdasdaaaaaaaaa'
    # создадим курс
    course = Course.objects.create(name=name_test)
    count_courses = Course.objects.count()

    id = course.id

    # удалим курс
    response = client.delete(reverse('courses-detail', args=[id]))
    assert response.status_code == status.HTTP_204_NO_CONTENT, response.content

    # смотрим, что количество курсов уменьшилось на единицу
    assert Course.objects.count() == count_courses - 1


# валидация на максимальное число студентов на курсе
@pytest.mark.django_db
@pytest.mark.parametrize(
    ["count_students", "status_code_expected"],
    (
            (2, status.HTTP_201_CREATED),
            (30, status.HTTP_400_BAD_REQUEST),
    )
)
def test_max_students_per_course(
        client,
        settings,
        student_factory,
        count_students,
        status_code_expected
):
    settings.MAX_STUDENTS_PER_COURSE = 2
    assert settings.MAX_STUDENTS_PER_COURSE

    name_test = 'test_max_students_per_course'
    students = student_factory(_quantity=count_students)
    students_id = [student.id for student in students]

    response = client.post(
        reverse('courses-list'),
        data={
            'name': name_test,
            'students': students_id,
        }
    )

    assert response.status_code == status_code_expected, response.content
