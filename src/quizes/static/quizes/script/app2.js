// Fetch data from Backend Service
async function fetchData() {
    const url = window.location.href + 'data/'
    try  {
        const response = await fetch(url)
        return await response.json()
    } catch(err) {
        console.log(err)
    }
}

// Render data to the quiz box
async function renderQuiz() {
    const quizBox = document.querySelector('.quiz-box')
    const {data} = await fetchData()
    data.forEach(el => {
        questionAnswerArray = Object.entries(el)
        questionAnswerArray.forEach(([question, answers]) => {
            quizBox.innerHTML += `
                <hr>
                <div class="mb-2">
                    <p><strong>${question}</strong></p>
                </div>
            `
            answers.forEach(answer => {
                quizBox.innerHTML += `
                    <div>
                        <input type="radio"
                               class="answer"
                               id="${question}-${answer}"
                               name="${question}"
                               value="${answer}"
                        />
                        <label for="${question}">
                            ${answer}
                        </label>
                    </div>
                `
            })
        })
    })
}

function submitQuizForm() {
    // Quiz form
    const quizForm = document.querySelector('#quiz-form')

    quizForm.addEventListener('submit', e => {
        e.preventDefault()
        // csrf token
        const csrf = document.querySelector('input[name=csrfmiddlewaretoken]')

        const answers = document.querySelectorAll('.answer')
        const answersArray = [...answers]

        const data = {}
        answersArray.forEach((ans) => {
            if (ans.checked) {
                data[ans.name] = ans.value
            } else {
                if (!data[ans.name]) {
                    data[ans.name] = null
                }
            }
        })
        const url = window.location.href + 'save/'

        fetch(url, {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf.value
            },
            body: JSON.stringify(data)
        }).then((resp) => {
            return resp.json()
        }).then(data => {
            const result = data.results
            quizForm.classList.add('hide')
            result.forEach(res => {
                const resultDiv = document.createElement('div')
                Object.entries(res).forEach(([question, answer]) => {
                    console.log(question, answer)

                })
            })
        }).catch(err => {
            console.log('An error occurred sending answers')
        })
    })
}

// Main wrapper function
function main() {
    renderQuiz()
    submitQuizForm()
}

// Call main function
main()