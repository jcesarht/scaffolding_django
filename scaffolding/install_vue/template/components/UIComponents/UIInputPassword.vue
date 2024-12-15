<template>
    <div class="w-full mb-2">
        <div v-if="showLabel" class="px-1 text-gray-500" >
            <strong>{{ fieldName }}</strong>
        </div>
        <div>
            <input
                :class="[
                    'font-semibold',
                    'w-full',
                    'rounded px-3 py-2 border-2',
                    borderColor,
                    'focus:outline-none',
                    focusBorderColor,
                    'text-sm',
                ]
                "
                :type="input_type"
                :name="input.name"
                :id="inputID"
                v-model="input_value"
                :placeholder="placeholderText"
                :required="input.required"
                :autocomplete="input.autocomplete"
                @input="validateInput()"
            />
        </div>
        <div class="px-1 min-h-6">
            <span :class="[
                'text-xs',
                'italic',
                'leading-1',
                colorText
                ]"
            >{{ input_sign }} </span>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, reactive } from 'vue';
    
    const input = defineProps(
        {
            'name' : {
                type: String,
                required: true,
                default: 'input'
            },
            'placeholder' : {
                type: String,
                default: 'Write something here ...'
            },   
            'id' : {
                type: String,
                default: ''
            },
            'value' : {
                type: String,
                default: ''
            },
            'field' : {
                type: String,
                default:''
            },
            'required' : {
                type: String,
                default: "false",
            },
            'rule' : {
                type: String,
                default: "all",
            },
            'ruleText' : {
                type: String,
                default: "",
            },
            'minChar' : {
                type: String,
                default: -1,
            },
            'maxChar' : {
                type: String,
                default: "-1",
            },
            'autocomplete' : {
                type: String,
                default: 'off',
            },
        }
    );

    //set all props handlely
    const input_value = defineModel()
    const inputID = ref((input.id == '')? input.name + '_id': input.id )
    const required = (input.required == "true") // assign true or false
    const rule = input.rule
    const input_type = 'password'
    const minChar = input.minChar
    const maxChar = input.maxChar
    const showLabel = ref( input.field && input.field.trim() != '' )
    input_value.value = input.value
    
    const isError= reactive({
        'typeError': null,
        'message':'',
        'error': false
    })

    //computed message over the input
    const input_sign = computed(()=>{
        return isError.error? isError.message: input.ruleText ;
    })

    // define computed border class
    const borderColor = computed(()=>{
        return (isError.error)? 'border-red-300' : 'border-blue-300'
    });

    const focusBorderColor = computed(()=>{
        return (isError.error )? 'focus:border-red-500' : 'focus:border-blue-500'
    })
    // computed color text
    const colorText = computed(()=>{
        return (isError.error)? 'text-red-500' : 'text-gray-500'
    })

    //computed placeholder
    const placeholderText = computed(()=>{
        let placeholder = String(input.placeholder).trim()
        return (
            required 
            && placeholder != '' 
            && String(input.field).trim() == "") ? placeholder + " *" : placeholder
    })
    
    //computed field name
    const fieldName = computed(()=>{
        let field = String(input.field).trim()
        return (required && field != '' )? field + " *" : field
    })

    let debounceTime = null;
    // define rules
    const validateInput = ()=>{
        validateRules()
        debouncedProcessInput(3000)
    }

    const debouncedProcessInput = (seconds)=>{
        clearTimeout(debounceTime)
        debounceTime = setTimeout(()=>{
            takeInputValue();  
        },seconds);
    }

    // take char by char and validate
    const takeInputValue = ()=>{
        validateRulesAfterInput()
        if(!isError.error){
            //execute some here
            //console.log(input_sign.value)
        }   
    }

    //validate rules
    const validateRules = () => {
        let exclude_character = '';
        let input_to_check = String(input_value.value).trim()
        input_to_check  = (input_to_check == 'undefined')? '' : input_to_check
        isError.typeError = ''
        isError.error = false
        isError.message = ''
        if (required && input_to_check == '' ) {
            input_value.value = String(input_to_check.replace(/\s?/,''));
            isError.typeError = 'empty'
            isError.error = true
            isError.message = 'Password is required'
        }else if (rule == 'alphanumeric') {
            //this sentence only alphanumerics plus "_" characters are accepted
            exclude_character = input_to_check.match(/[^A-Z-a-z-0-9ñÑ\_]/)
            exclude_character = exclude_character == null? '' : exclude_character
            input_value.value = String(input_to_check.replace(/[^A-Z-a-z-0-9ñÑ\_]/,''));
            if (exclude_character != null && exclude_character.length > 0){
                isError.typeError = 'alphanumeric'
                isError.error = true
                isError.message = exclude_character + ' is not allowed'
            }
        }else if (rule == 'numeric'){
            exclude_character = input_to_check.match(/[^0-9]/)
            exclude_character = exclude_character == null? '' : exclude_character
            input_value.value = String(input_to_check.replace(/[^0-9]/,''))
            if (exclude_character.length > 0){
                isError.typeError = 'numeric'
                isError.error = true
                isError.message = exclude_character + ' is not numeric; therefore, it is not allowed'
            }
        }
    }

    //validate maximum and minimum char 
    const validateRulesAfterInput = ()=> {
         // validate minimun characters
         if (minChar > 0 && input_value.value.length < minChar){
            isError.typeError = 'minimun_chars'
            isError.error = true
            isError.message = 'Please enter at least '+ minChar +' characters'
        }
        
        // validate maximum characters
        if (maxChar > 0 && input_value.value.length > maxChar){
            isError.typeError = 'maximun_chars'
            isError.error = true
            isError.message = 'Please enter no more than '+ maxChar +' characters'
        }

    }

     /**
    * validate if an error exist and return a boolean
    */
    const  checkValidateError = ()=>{
        validateRules()
        validateRulesAfterInput()
        return isError.error
    }
    
    // return the input value to parent
    const valueInput = ()=>{
        return input_value.value;
    }
    // expose the checkValidateError to parent component
    defineExpose({checkValidateError,valueInput})
</script>

<style lang="scss" scoped>
</style>