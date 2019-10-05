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

shuviscript can be written in below formation(which defined a stacked auto encoder of two layers):

```
input=(output)()input_pipe()
lay1=(encode, decode, train)(studyrate)sae_relu(input.output)
lay2=(encode, decode, train)(studyrate)sae_tanh(lay1.encode)
```

how to understand above script:

```
<node-name>=<output-list><placeholder-list><method-name><input-list>
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

---
