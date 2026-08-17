import {
  Component,
  EventEmitter,
  Input,
  Output
} from '@angular/core';

import { FormsModule } from '@angular/forms';


@Component({
  selector: 'app-composer',

  standalone: true,

  imports: [
    FormsModule
  ],

  templateUrl: './composer.html',

  styleUrl: './composer.css'
})
export class Composer {

  @Input()
  question = '';

  @Input()
  loading = false;

  @Output()
  questionChange = new EventEmitter<string>();

  @Output()
  sendRequested = new EventEmitter<void>();


  onQuestionChange(value: string) {

    this.question = value;

    this.questionChange.emit(value);

  }


  send() {

    if (
      this.loading ||
      !this.question.trim()
    ) {
      return;
    }

    this.sendRequested.emit();

  }


  handleEnter(event: Event) {

    const keyboardEvent =
      event as KeyboardEvent;

    if (!keyboardEvent.shiftKey) {

      keyboardEvent.preventDefault();

      this.send();

    }

  }

}