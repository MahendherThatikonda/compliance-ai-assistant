import {
  Component,
  EventEmitter,
  Input,
  Output
} from '@angular/core';

import { CommonModule } from '@angular/common';
import { Suggestion } from '../suggestion/suggestion';

type Page = 'home' | 'standards' | 'about';

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [
    CommonModule,
    Suggestion
  ],
  templateUrl: './sidebar.html',
  styleUrl: './sidebar.css'
})
export class Sidebar {

  @Input()
  currentPage: Page = 'home';

  @Input()
  examples: string[] = [];

  @Output()
  navigatePage = new EventEmitter<Page>();

  @Output()
  newChatRequested = new EventEmitter<void>();

  @Output()
  exampleSelected = new EventEmitter<string>();


  navigate(page: Page) {
    this.navigatePage.emit(page);
  }


  newChat() {
    this.newChatRequested.emit();
  }


  selectExample(example: string) {
    this.exampleSelected.emit(example);
  }


}