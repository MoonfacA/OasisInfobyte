window.addEventListener('load', ()=>{
    const form= document.querySelector("#task-form");
    const input= document.querySelector("#task-input");
    const taskDateInput = document.getElementById("taskDate");
    const list= document.querySelector("#tasks");
    const completedContainer = document.getElementById("completedList");
    

    
    form.addEventListener('submit', (e)=>{
        e.preventDefault();//Prevents form from submitting

        const task = input.value;
        if (!task) {
            alert("Task cannot be empty, please click ok then add input to task.");
        }else{
        
        const task_div = document.createElement("div");
        task_div.classList.add("task");
        list.appendChild(task_div);

        const taskDate = taskDateInput.value;
        if (!taskDate) {
            alert("Due time cannot be empty");
           
        }else{
        // Parse the selected date and the current date
        const selectedDate = new Date(taskDate);
        const currentDate = new Date();
        selectedDate.setHours(0, 0, 0, 0); // Set time part to midnight
        currentDate.setHours(0, 0, 0, 0);
  
        // Compare the selected date with the current date
        if (selectedDate < currentDate && selectedDate !== currentDate) {
            alert(
                "Oops! enter valid date"
              );
              return;
        }
    }


        const task_content_div = document.createElement("div");
        task_content_div.classList.add("content");
        task_content_div.innerHTML = "Due: " + taskDate;
        if (!taskDate) {
            list.removeChild(task_div);
        }else{
        task_div.appendChild(task_content_div);
    }
   

        const task_input= document.createElement("input");
        task_input.classList.add("text");
        task_input.type = "text";
        task_input.value= task;
        task_input.setAttribute("readonly", "readonly");
        task_content_div.appendChild(task_input);

        
       

        const task_actions_div= document.createElement("div");
        task_actions_div.classList.add("actions");
        task_div.appendChild(task_actions_div);

        const task_edit_botton= document.createElement("button");
        task_edit_botton.classList.add("Edit");
        task_edit_botton.innerHTML = "Edit";

        const task_delete_button= document.createElement("button");
        task_delete_button.classList.add("Delete");
        task_delete_button.innerHTML = "Delete";

        const task_completed_button= document.createElement("button");
        task_completed_button.classList.add("Completed");
        task_completed_button.innerHTML = "Completed";

        const now = new Date()
        const currentDateTime = now.toLocaleString();

        const task_edit_botton1= document.createElement("button");
        task_edit_botton1.classList.add("Edit1");
        task_edit_botton1.innerHTML = "Task Uploaded: " + currentDateTime;
        

        task_actions_div.appendChild(task_edit_botton1);
        task_actions_div.appendChild(task_edit_botton);
        task_actions_div.appendChild(task_completed_button);
        task_actions_div.appendChild(task_delete_button);
        

    
       

        task_edit_botton.addEventListener('click', ()=>{
            
            if (task_edit_botton.innerText.toLowerCase() =="edit") {
                    task_input.removeAttribute("readonly");
                    task_input.focus();
                    task_edit_botton.innerText = "Save";
                    task_input.style.textDecoration="none"
            }else{
                task_input.setAttribute("readonly", "readonly");
                task_edit_botton.innerText ="Edit";
                
            }
        });

        task_delete_button.addEventListener('click', ()=>{
            if (confirm("Are you sure you want to delete this task?")) {
                list.removeChild(task_div);
                

            }
        })
        
        task_completed_button.addEventListener('click', ()=>{
            
                task_input.style.textDecoration="line-through";
                task_input.setAttribute("readonly", "readonly");

                const task_inputCopy = task_input;
                const completedList = document.getElementById("completedbody");
                completedList.appendChild(task_inputCopy);      
               
        })

   
        input.value = "";
        taskDateInput.value = "";
        
        }

    });
    //*Event listener for  filter*//
    // Function to add completed task to the completed list
    function addToCompleted(taskItem) {
        const completedList = document.getElementById("completedbody");
        completedList.appendChild(taskItem);
      }
    
      // Function to remove completed task from the completed list
      function removeFromCompleted(taskItem) {
        const completedList = document.getElementById("completedbody");
        completedList.removeChild(taskItem);
      }
    
});