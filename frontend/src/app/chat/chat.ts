import {
  Component,
  EventEmitter,
  Input,
  Output
} from '@angular/core';

import { CommonModule } from '@angular/common';


export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  time: string;

  liked?: boolean;
  showSources?: boolean;

  sources?: string[];
}


@Component({
  selector: 'app-chat',

  standalone: true,

  imports: [
    CommonModule
  ],

  templateUrl: './chat.html',

  styleUrl: './chat.css'
})
export class Chat {

  @Input()
  messages: ChatMessage[] = [];


  @Input()
  loading = false;


  @Output()
  copyRequested = new EventEmitter<string>();


  toggleLike(message: ChatMessage) {

    message.liked = !message.liked;

  }


  toggleSources(message: ChatMessage) {

    message.showSources = !message.showSources;

  }


  copyAnswer(content: string) {

    this.copyRequested.emit(content);

  }

  hasEnoughInformation(message: any): boolean {
  return !message.content
    ?.toLowerCase()
    .includes('not enough information');
}

}