# Waldo!

[![Build Status](https://travis-ci.org/Alir3z4/waldo.svg?branch=master)](https://travis-ci.org/Alir3z4/waldo)
[![codecov](https://codecov.io/gh/Alir3z4/waldo/branch/master/graph/badge.svg)](https://codecov.io/gh/Alir3z4/waldo)


Finds the cropped image in the original one.

Made with ❤ and powered by [OpenCV](https://opencv.org/).

### Installing

Clone the repo and install.

* `$ git clone git@github.com:Alir3z4/waldo.git && cd waldo`
* `$ python setup.py install`


### Usage via CLI

The usage via CLI is pretty simple:

```
Usage: subimage image1.jpeg image2.jpeg --display[Optional]
```

Args `--display` will give you a nice tiny graphical window to show the result.

Once installed, the binary `subimage` will be available in the path.

To find the top left position:

```
$ subimage images\landing.JPG images\landing-face.JPG
```

You can also pass `--display` arg to enable graphical interface to show the result.

```
$ subimage images\landing.JPG images\landing-face.JPG
```


## Using as Library

You can use functionality as an standalone library as well in other programs.

```
>>> from subimage import SubImage
>>> sub_image = SubImage(first_image_path='images/puzzle.png', second_image_path='images/waldo.png')
>>> sub_image.find_match()
>>> sub_image.tell_top_left()
Top Left: (1300, 852)
>>> sub_image.display() # It will open up a graphical window and shows the result
Exit with pressing 0 (zero).
```
 

### Development

In case you don't want to install the library would like to try it:

* `$ git clone git@github.com:Alir3z4/waldo.git && cd waldo`
* `$ pip install -r requirements-dev.txt`

Since you have not installed it, therefore no `subimage` binary/script will be available, in order to access it, call
 the `sumimage.py` as follow:

```
$ python subimage.py image1.jpeg image2.jpeg --display[Optional]
```

#### Tests

The implementation is well tested and all the tests can be run via:

```
$ python setup.py test
```


#### Code Coverage

To review the code coverage report run:

```
python setup.py coverage
```

It will generate the code coverage, printed on screen and saved in HTML format under `htmlcov/` dir. 


### CI

On every push travis-CI will trigger the tests and report the code coverage.
