const API = "http://3.109.152.74:5000";

async function loadTodos() {
    const response = await fetch(`${API}/todos`);
    const data = await response.json();

    const list = document.getElementById("todoList");
    list.innerHTML = "";

    data.forEach(todo => {
        const li = document.createElement("li");
        li.innerText = todo.task;
        list.appendChild(li);
    });
}

async function addTodo() {
    const taskInput = document.getElementById("task");
    const task = taskInput.value;

    if (!task) {
        alert("Enter a task!");
        return;
    }

    await fetch(`${API}/todos`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ task: task })
    });

    taskInput.value = "";
    loadTodos();
}

window.onload = loadTodos;
