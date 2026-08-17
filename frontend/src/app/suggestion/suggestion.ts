import {
  ChangeDetectorRef,
  Component
} from '@angular/core';

import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import {
  HttpClient,
  HttpClientModule
} from '@angular/common/http';

@Component({
  selector: 'app-suggestion',
  standalone: true,

  imports: [
    CommonModule,
    FormsModule,
    HttpClientModule
  ],

  templateUrl: './suggestion.html',
  styleUrl: './suggestion.css'
})
export class Suggestion {

  suggestion = '';

  isOpen = false;

  sending = false;

  successMessage = '';

  errorMessage = '';


  constructor(
    private http: HttpClient,
    private cdr: ChangeDetectorRef
  ) {}


  openSuggestion() {

    this.isOpen = true;

    this.successMessage = '';
    this.errorMessage = '';

  }


  closeSuggestion() {

    this.isOpen = false;

    this.suggestion = '';

    this.successMessage = '';
    this.errorMessage = '';

    this.sending = false;

  }


  submitSuggestion() {

    const text = this.suggestion.trim();

    if (!text || this.sending) {
      return;
    }


    this.sending = true;

    this.successMessage = '';
    this.errorMessage = '';

    this.cdr.detectChanges();


    this.http.post(
      'https://compliance-ai-assistant.onrender.com/suggestion',
      {
        suggestion: text
      }
    )
    .subscribe({

      next: () => {

        console.log(
          'Suggestion successfully sent'
        );

        this.sending = false;

        this.suggestion = '';

        this.successMessage =
          'Thanks! Your suggestion has been sent.';

        this.cdr.detectChanges();

      },


      error: (error) => {

        console.error(
          'Suggestion error:',
          error
        );

        this.sending = false;

        this.errorMessage =
          'Could not send your suggestion. Please try again.';

        this.cdr.detectChanges();

      }

    });

  }

}