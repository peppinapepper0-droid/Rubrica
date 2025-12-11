async function login() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const res = await fetch("/api/login", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({email, password})
    });

    const data = await res.json();
    alert(data.message || data.error);

    if (res.status === 200)
        location.href = "tasks.html";
}

async function registerUser() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const res = await fetch("/api/register", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({email, password})
    });

    const data = await res.json();
    alert(data.message || data.error);

    if (res.status === 201)
        location.href = "login.html";
}


async function logout() {
    await fetch("/api/logout", {method: "POST"});
    location.href = "login.html";
}

//MODIFICO FUNZIONE PER CARICARE I MSG SUL SERVER
async function loadTasks() {

    const res = await fetch("/api/tasks"); //richiesta Get

    if (res.status !== 200) {
        location.href = "login.html"; //manda alla pagina di login
        return;
    }

    const data = await res.json(); //converte risposta in Json
    const list = document.getElementById("taskList");   //prende elemento riferito alla lista dei messaggi (taskList nell'html) e la svuota per evitare doppioni
    list.innerHTML = "";

    //trovo utente loggato
    const utente= data.creatore;

    data.items.forEach(t => {   //scorro ogni task edl server e per ognuno crea un contenitore "li"
        const li = document.createElement("li");
        li.className = t.done ? "done" : "";    //se task è completato mette "done"

        // Testo
        const textSpan = document.createElement("span");    //creo oggetto "span" che contiene messaggio
        textSpan.textContent = `${t.autore} - ${t.date} = ${t.text}`;   //aggiungo autore, data e contenuto del messaggio

        // Area icone
        const actions = document.createElement("div");  //contenuto icone

        // 🗑 icona
        if (t.cestino === utente){    //se messaggio appartiene a utente loggato, mostra icona cestino
            //creazione icona
            const del = document.createElement("button");
            del.className = "icon-btn";
            del.innerHTML = '<i class="fa-solid fa-trash" title="Elimina"></i>';
            //quando ci clicco sopra viene eliminato messaggio
            del.onclick = () => deleteTask(t.id);
            //aggiunta bottone a contenitore icone(actions)
            actions.appendChild(del);
        }

        //aggiungo testo del messaggio + contenitore icone a li
        li.appendChild(textSpan);
        li.appendChild(actions);
        //agguinge il li alla lista html (taskList)
        list.appendChild(li);
    });
}

async function addTask() {
    const text = document.getElementById("taskText").value;

    await fetch("/api/tasks", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({text})
    });

    loadTasks();
}



async function deleteTask(id) {
    await fetch(`/api/tasks/${id}/delete`, {method: "DELETE"});
    loadTasks();
}

if (location.pathname.endsWith("tasks.html"))
    loadTasks();
