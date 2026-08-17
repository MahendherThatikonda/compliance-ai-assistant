import { Component, ChangeDetectorRef } from '@angular/core';
import { Chat, ChatMessage } from './chat/chat';
import { Composer } from './composer/composer';
import { Sidebar } from './sidebar/sidebar';
import { Welcome } from './welcome/welcome';
import { Standards } from './standards/standards';
import { About } from './about/about';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { finalize } from 'rxjs';


type Page = 'home' | 'standards' | 'about';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    Chat,
    Composer,
    Sidebar,
    Welcome,
    Standards,
    About,
    HttpClientModule   
  ],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {

  currentPage: Page = 'home';

  question = '';
  loading = false;

  messages: ChatMessage[] = [];

  examples = [
    'What are the requirements for gully traps?',
    'What is the required water seal for a gully?',
    'What are the requirements for floor waste gullies?',
    'What are the backflow prevention requirements?',
    'What are the vent pipe sizing requirements?'
  ];

  constructor(
    private http: HttpClient,
    private cdr: ChangeDetectorRef
  ) {}

  navigate(page: Page) {
    this.currentPage = page;
  }

  useExample(example: string) {
    this.currentPage = 'home';
    this.question = example;
  }

  askQuestion() {

    const text = this.question.trim();

    if (!text || this.loading) {
      return;
    }

    this.currentPage = 'home';

    this.messages = [
      ...this.messages,
      {
        role: 'user',
        content: text,
        time: this.getCurrentTime()
      }
    ];

    this.question = '';
    this.loading = true;

    this.http.post<any>(
      'https://compliance-ai-assistant.onrender.com/ask',
      {
        question: text
      }
    )
    .pipe(
      finalize(() => {
        this.loading = false;
        this.cdr.detectChanges();
      })
    )
    .subscribe({

next: (response) => {

  let answer = '';
  let sources: string[] = [];

  if (typeof response === 'string') {

    answer = response;

  }
  else if (response?.answer) {

    answer = response.answer;

    sources = response.sources || [];

  }
  else if (response?.response) {

    answer = response.response;

    sources = response.sources || [];

  }
  else {

    answer = JSON.stringify(response);

  }


  this.messages = [
    ...this.messages,
    {
      role: 'assistant',
      content: answer,
      time: this.getCurrentTime(),
      sources: sources
    }
  ];

  this.cdr.detectChanges();
},

      error: (error) => {

        console.error('API ERROR:', error);

        this.messages = [
          ...this.messages,
          {
            role: 'assistant',
            content:
              'Sorry, I could not retrieve the compliance information. Please try again.',
            time: this.getCurrentTime()
          }
        ];

        this.cdr.detectChanges();
      }

    });
  }

//   sendSuggestion(text: string) {

//   this.http.post(
//     'http://127.0.0.1:8000/suggestion',
//     {
//       suggestion: text
//     }
//   )
//   .subscribe({

//     next: () => {
//       console.log('Suggestion sent successfully');
//     },

//     error: (error) => {
//       console.error('Suggestion failed:', error);
//     }

//   });

// }

  handleEnter(event: Event) {

    const keyboardEvent = event as KeyboardEvent;

    if (!keyboardEvent.shiftKey) {
      keyboardEvent.preventDefault();
      this.askQuestion();
    }
  }

  copyAnswer(content: string) {
  navigator.clipboard
    .writeText(content)
    .then(() => {
      console.log('Answer copied');
    })
    .catch(error => {
      console.error('Copy failed:', error);
    });
}

  newChat() {
    this.currentPage = 'home';
    this.messages = [];
    this.question = '';
  }

  getCurrentTime(): string {

    return new Date().toLocaleTimeString([], {
      hour: '2-digit',
      minute: '2-digit'
    });
  }
}