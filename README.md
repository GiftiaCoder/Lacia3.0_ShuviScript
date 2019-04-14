# Lacia3.0_ShuviScript

---

## abstract

did you feel your code is too mess to build a model ?

there are always over a thousand of lines in just one or some few py files, and relationship between lines are hard to organize .

lacia project will entirely restructured by a tiny script named ShuviScript, join us !

---

## simple introduction of ShuviScript

shuvicript can be split into three part: script, method and configure

### script

shuviscript is just a Graph Description Launguage, which works just like UML to descibe a link graph of a model . it is said that, shuviscript cannot define the real logic of a model .

shuviscript can be written in below formation(which defined a stacked auto encoder of two layers):

```
input=(output)()input_pipe()
lay1=(encode, decode, train)(studyrate)sae_relu(input.output)
lay2=(encode, decode, train)(studyrate)sae_tanh(lay1.encode)
```

how to understand above script:

```
<node-name>=<output-list><placeholder-list><method-name><input-ist>
```

### ShuviMethod

shuvi method defined the real logic of a model , which can be written by OO .

you just need to inherit class shuvi.method.method.ShuviMethod , and override function: __constructor__, __init__ and __update_conf__ , like below:

```python
class OutputMethod(method.ShuviMethod):
    def __init__(self, name, graph, inputs):
        super().__init__(name, graph, inputs)

        offset = tf.placeholder(tf.float32)
        self.register_placeholder('offset', offset)

        input = inputs['input.output']
        output = input * input + offset
        self.register_output('output', output)
```

### configure

#### i will complete any longer (笑)

---