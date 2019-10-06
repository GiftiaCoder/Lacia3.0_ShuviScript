# ShuviScript

---

## abstract

did you feel your code too mess to build a model ?

there are always over a thousand of lines in just one or some few py files, and relationship between tensors are hard to organize .

***ShuviScript*** provide a new way for developers to build models with ***Object Oriented*** design .

care ! we just support tensorflow 1.0 currently .

---

## simple introduction of ShuviScript

shuvicript can be split into three part: scripts, methods and configures

you can see ***sample.py*** as an exampe

### script

shuviscript is just a ***Graph Description Launguage***, which works just like UML to descibe the graph of a model . it is said that, shuviscript cannot define the real logic of a model .

shuviscript should be written in the formation below :

```python
<node-name>=<output-list><placeholder-list><method-name><input-list>
```

for example :

```python
# define a input node
input = (output)()input_method()
# use input.output as input to build an other output node
output = (output)(offset)output_method(input.output)
```

#### node-name

the name of current node

#### method-name

the method of current node

a <method-name, Method-Constructor> relation should be given to Graph

```python
class OutputMethod(shuvi.method.method.Method):
    def __init__(self, inputs, inputnodes, confs, conf, logger):
        super().__init__(inputs, inputnodes, confs, conf, logger)

        # to create the placeholder: offset
        # offset(in method) => offset(in script)
        self.offset = tf.placeholder(dtype=tf.float32)
        self.register_placeholder('offset', self.offset)

        # to create to output: output
        # output(in method) => output(in script)
        self.output = inputs[0] * tf.sin(inputs[0]) + self.offset
        self.register_output('output', self.output)

    # be careful ! 
    # if your Method need a placeholder
    # you should also need to implement a feed_dict method to set the placeholder
    def feed_dict(self, feeddict):
        feeddict[self.offset] = 3.141
```

#### output-list

the ***output-name*** in script should be equal to to ***output-name*** in ***class Method***

#### placeholder-list

the ***placeholder-name*** in script should be equal to to ***placeholder-name*** in ***class Method***

#### input-list

a reference list to the ***nodes*** and their ***outputs*** that have been defined

an ***input*** should be written in the formation below :

```
<node-name>.<output-name>
```

### Method

just like the section ***method-name*** above

there are 4 method you can inherit in ***class Method*** : ***constructor***, ***init***, ***conf*** and ***feed_back***

#### constructor

you should build your outputs and placeholders here

you can also do something else

#### init

if there is something need initialized with a ***Session***, do it here

#### conf

load conf data here

***confs*** is a dict of global conf data

***conf*** is a child in ***confs***, which only contain to data of current node, and of course, it's also a dict

```python
# you can inherit the conf metdhod like this
# with the example in method-name section above
def conf(self, confs, conf):
    self.val_offset = conf['offset']
```

#### feed_dict

to fill the ***feed_dict*** before ***Session.run***

if current node provide any placeholders, you should inherit this method

```python
# with the example in conf section, you can write your feed_dict method like tihs
def feed_dict(self, feeddict):
    feeddict[self.offset] = self.val_offset
```

### Configure

i'll complete any further (笑)

---
